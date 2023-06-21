import calendar
import json
import logging
import time
from requests.exceptions import ConnectionError

from notifications.signals import notify
from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source

from django.shortcuts import reverse
from django.utils import timezone

from api.utils import generate_certificate_image
from blockchain import settings
from blockchain.models import Contract, CertificateAddress
from digiinsurance.models import Enrollment, User
# from digiinsurance.notifications import (
#     VERBS, DESCRIPTIONS, SCHOOL_DESCRIPTIONS)

logger = logging.getLogger('blockchain')

try:
    web3 = Web3(Web3.HTTPProvider(settings.RPC))
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    web3.net.version
except ConnectionError as e:
    raise e

COINBASE = web3.eth.coinbase


def get_accounts():
    # Get all accounts stored in the node connected to web3
    return web3.eth.accounts


def create_account(passphrase):
    return web3.personal.newAccount(passphrase)


def get_balance(address, in_ether=True):
    # Get Ether balance of account
    if in_ether:
        return web3.fromWei(web3.eth.getBalance(address), "ether")
    else:
        return web3.eth.getBalance(address)


def wait(tx, contract=False):
    # Wait for Transaction requested to the blockchain
    # Set contract to True if the transaction pending is a contract
    # deployment. Leave False if normal function/transaction call
    try:
        receipt = web3.eth.waitForTransactionReceipt(tx, timeout=60)
        timestamp = web3.eth.getBlock(receipt['blockNumber']).timestamp
        if receipt['status'] == 1:
            if contract:
                logger.info(
                    "Contract Deployment SUCCESS [%s]",
                    receipt['contractAddress'])
                return receipt['contractAddress']

            else:
                logger.info(
                    "Transaction SUCCESS [%s]",
                    receipt['transactionHash'].hex())
                return True, receipt['transactionHash'].hex(), timestamp
        else:
            logger.error(
                "Transaction FAIL [%s]", receipt['transactionHash'].hex())
            return False, receipt['transactionHash'].hex(), timestamp

    except Exception as e:
        logger.error(e)
        raise e


def send_ether(_to, _from=COINBASE, value=1):
    # Send Ether to _to address.
    # Make sure web3 connected has access to coinbase with enough ethers.
    tx = web3.eth.sendTransaction({
        'from': _from,
        'to': _to,
        'value': web3.toWei(value, "ether")
    })

    return wait(tx)


def save_contract(address, name, abi):
    # Save Contract template to DB
    # This stores the address and ABI of a contract template
    try:
        contract, created = Contract.objects.update_or_create(
            name=name,
            defaults={
                'address': address,
                'owner': web3.eth.coinbase,
                'abi': json.dumps(abi)})
        return contract

    except Exception as e:
        logger.error(e)
        raise e


def deploy_contract(
        contract_source, contractName, constructorArgs=[], transactArgs={}):
    # If successful, returns Contract Address, and ABI

    with open(contract_source, 'r') as f:
        source = f.read()

    compiled_sol = compile_source(source)
    contract_interface = compiled_sol['<stdin>:%s' % contractName]

    Contract = web3.eth.contract(
        abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = Contract.constructor(*constructorArgs).transact(transactArgs)
    tx_receipt = wait(tx_hash, contract=True)

    return tx_receipt, contract_interface['abi']


def get_coin_contract():
    # Gets APPCoin Interface
    try:
        contract = Contract.objects.get(name='AppCoin')
        address = contract.address
        abi = json.loads(contract.abi)

        return web3.eth.contract(address=address, abi=abi)

    except Exception as e:
        logger.error("Coin Contract Not Found!")
        raise e


def mint_coins(_to, value=100):
    # Minter Account (COINBASE) will mint coin and send to _to address.
    # Note: APPCoin divisibility is 2, i.e, minting value of 100 is equivalent
    # to 1 APPCoin
    COIN = get_coin_contract()
    tx = COIN.functions.mint(web3.toChecksumAddress(_to), value).transact({
        'from': COINBASE
    })

    return wait(tx)


def get_coins(address):
    # Gets Coin Balance of an account address
    COIN = get_coin_contract()
    return COIN.functions.balanceOf(address).call()


def send_coins(_from, _to, value, passphrase):
    # Send Coin to an account address.
    # Used when buying courses using the coins.
    COIN = get_coin_contract()
    if get_coins(_from) >= value:
        # User should unlock their account using their set passphrase.
        # Locked account won't be able to spend coins on it!
        if web3.personal.unlockAccount(_from, passphrase, duration=15):
            tx = COIN.functions.transfer(_to, value).transact({
                'from': _from
            })
            return wait(tx)
        else:
            logger.info('Account %s is LOCKED!' % _from)
            return False
    else:
        logger.error('Account %s has INSUFFICIENT BALANCE' % _from)
        return False


def total_supply():
    COIN = get_coin_contract()
    return COIN.functions.totalSupply().call()


def get_certificate(address):
    # Gets Certificate details stored in the address at the blockchain
    try:
        cert = Contract.objects.get(name="Certificate")
        abi = json.loads(cert.abi)

        CERT = web3.eth.contract(address=address, abi=abi)
        # date = time.strftime(
        #     '%Y-%m-%-d %H:%M:%S', time.localtime(
        #         CERT.functions.receiveDate().call()))

        details = {
            'full_name': CERT.functions.fullName().call(),
            'course': CERT.functions.course().call(),
            'school': CERT.functions.school().call(),
            'valid': CERT.functions.valid().call(),
            'class': CERT.functions.className().call(),
            'date': CERT.functions.receiveDate().call(),
        }

        return details

    except Exception as e:
        logger.error("Certificate %s NOT FOUND!" % address)
        raise e


def create_certificate(enrollment_id, date=None):
    from api.tasks.email import send_certificate_generation_email
    # Certificate Factory
    # constructorArgs should contain the certificate data, in order:
    # [issuer, fullName, courseName, schoolName, className, date(in epoch)]
    # date is in format "MM-dd-YYYY"
    details = Enrollment.objects.get(id=enrollment_id)
    student = details.student.full_name
    course = details.get_course()
    clss = details.get_course()
    school = course.school.name
    if details.date_completed:
        ts = details.date_completed
        epoch = int(ts.timestamp())
    elif date:
        ts = date
        epoch = int(ts.timestamp())
    else:
        ts = timezone.now()
        epoch = calendar.timegm(time.gmtime())

    conArgs = [COINBASE, student, course.name, school, clss.name, epoch]
    transArgs = {'from': COINBASE}

    try:
        rcpt, abi = deploy_contract(
            'blockchain/contracts/Certificate.sol',
            'Certificate', constructorArgs=conArgs, transactArgs=transArgs)

        certificate, created = CertificateAddress.objects.update_or_create(
            enrollment=details,
            course=details.get_course(),
            student=details.student,
            available=False,
            defaults={'address': rcpt, 'timestamp': ts})

        if course.auto_certificate:
            certificate.available = True
            certificate.save(update_fields=['available'])
            generate_certificate_image(certificate.address)
            send_certificate_generation_email.delay(
                enrollment_id, certificate.id)

        return certificate

    except Exception as e:
        logger.error(e)
        raise e
