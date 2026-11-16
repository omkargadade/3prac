// SPDX-License-Identifier: MIT
// ^ License identifier. Solidity shows a warning in Remix if this line is missing.

pragma solidity ^0.8.0;
// ^ Tells the compiler which Solidity version to use.
//   ^0.8.0 means version 0.8.0 or any newer 0.8.x version.

// A "contract" is like a class in Java/Python. It holds data (variables)
// and behaviour (functions), and lives on the blockchain after deployment.
contract StudentManagement {

    // ---------------- STRUCTURE ----------------
    // A struct is a custom data type that groups related fields together,
    // like a class with only variables, or a C struct.
    struct Student {
        uint stud_id;        // uint = unsigned integer (no negative numbers)
        string name;         // student's name
        string department;   // student's department
    }

    // ---------------- ARRAY ----------------
    // A dynamic array that stores many Student structs.
    // "public" makes Solidity auto-create a getter function, so you can
    // read students[0], students[1], ... directly from Remix.
    Student[] public students;

    // ---------------- EVENTS ----------------
    // Events write a log entry to the blockchain. They are cheap and
    // useful for tracking what happened (you can see them in the Remix console).
    event StudentAdded(uint stud_id, string name, string department);
    event FallbackCalled(address sender, uint amount, bytes data);

    // ---------------- ADD A STUDENT ----------------
    // "public" means anyone can call this function.
    // "memory" means the strings are temporary copies that exist only
    // while the function runs (required for string parameters).
    function addStudent(uint _id, string memory _name, string memory _department) public {
        // Create a Student struct from the inputs and add it to the array.
        students.push(Student(_id, _name, _department));

        // Log that a student was added.
        emit StudentAdded(_id, _name, _department);
    }

    // ---------------- GET A STUDENT BY ID ----------------
    // "view" means the function only reads data and does not change it,
    // so calling it from outside costs no gas.
    // "returns (string memory, string memory)" means it gives back 2 values.
    function getStudent(uint _id) public view returns (string memory, string memory) {

        // Loop through the whole array one student at a time.
        for (uint i = 0; i)