from decimal import Decimal

POLICY_FEE = Decimal(400)
PAYMENT_TERM_MULTIPLIER = {
    'annual': Decimal(1),
    'semi_annual': Decimal(0.53),
    'quarterly': Decimal(0.275),
    'monthly': Decimal(0.0975),
}
DEFAULT_AGENT_CODE = '12390822'
SUPPORT_EMAIL = 'digiinsurance@qymera.com'
AGENT_EMAILS = [
    'digiinsurance@qymera.com',
    'digiinsurance1@qymera.com',
]
