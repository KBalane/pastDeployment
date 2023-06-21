pragma solidity ^0.4.24;

contract Certificate {

    address public issuer;
    bool public valid;

    string public fullName;
    string public course;
    string public school;
    int public receiveDate;
    string public className;

    constructor(address _issuer, string _fullName, string _course,
        string _school, string _className, int _date) public {
        issuer = _issuer;
        fullName = _fullName;
        course = _course;
        school = _school;
        receiveDate = _date;
        valid = true;
        className = _className;
    }

    modifier isIssuer() {
        require (msg.sender == issuer);
        _;
    }

    function revoke() external isIssuer {
        valid = false;
    }

    function fullName() public view returns (string) {
        return fullName;
    }

    function course() public view returns (string) {
        return course;
    }

    function school() public view returns (string) {
        return school;
    }

    function valid() public view returns (bool) {
        return valid;
    }

    function className() public view returns (string) {
        return className;
    }

    function receiveDate() public view returns (int) {
        return receiveDate;
    }
}