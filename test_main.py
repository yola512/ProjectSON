import os
import pytest
import csv
from typing import List, Dict
from mock_storage import MockCSVStorage
from main import import_from_file, export_attendance, add_student, edit_student, manage_attendance

@pytest.fixture
def csv_file():
    file = "students_test.csv"
    open(file, 'w').close()
    yield file
    os.remove(file)


class TestAttendanceSystem:
    #test: saving to file
    def test_save_to_file(self, csv_file):
        #Given
        students = [
              {"first_name": "John", "last_name": "Doe", "present": True},
              {"first_name": "Jane", "last_name": "Smith", "present": False},
        ]

        #When
        export_attendance(students, csv_file)

        #Then
        expected_data = [
           {"first_name": "John", "last_name": "Doe", "present": "yes"},
           {"first_name": "Jane", "last_name": "Smith", "present": "no"}, 
        ]
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            actual_data = [row for row in reader]

        assert actual_data == expected_data

    #test: loading from file
    def test_load_from_file(self, csv_file):
        #Given
        students = [
                {"first_name": "John", "last_name": "Doe", "present": "yes"},
                {"first_name": "Jane", "last_name": "Smith", "present": "no"},
            ]
        
        with open(csv_file, 'w', newline='') as file:
           fieldnames = ["first_name", "last_name", "present"]
           writer = csv.DictWriter(file, fieldnames)
           writer.writeheader()
           writer.writerows(students) 

        #When
        students_from_file = import_from_file(csv_file)

        #Then
        expected_students = [
                 {"first_name": "John", "last_name": "Doe", "present": True},
                 {"first_name": "Jane", "last_name": "Smith", "present": False},
            ]

        assert students_from_file == expected_students

    #test: adding students
    def test_add_students(self):
        #Given
        mock_storage = MockCSVStorage()
        mock_storage.write([
                    {"first_name": "John", "last_name": "Doe", "present": "yes"},
                ])

        #When
        add_student("Jane", "Smith", mock_storage)

        #Then
        expected_data = [
                    {"first_name": "John", "last_name": "Doe", "present": "yes"},
                    {"first_name": "Jane", "last_name": "Smith", "present": "no"},
                ]
        assert mock_storage.data == expected_data

    #test: editing students' data
    def test_edit_student(self):
        #Given
        mock_storage = MockCSVStorage()
        mock_storage.write([
                         {"first_name": "John", "last_name": "Doe", "present": "yes"},
                         {"first_name": "Jane", "last_name": "Smith", "present": "no"},
                    ])

        #When
        edit_student("Jane", "Smith", "Janet", "Smith", mock_storage)

        #Then
        expected_data = [
                        {"first_name": "John", "last_name": "Doe", "present": "yes"},
                        {"first_name": "Janet", "last_name": "Smith", "present": "no"},

                    ]
        assert mock_storage.data == expected_data
    
    #test: attendance
    def test_attendance_management(self):
        # Given
        mock_storage = MockCSVStorage()
        mock_storage.write([
            {"first_name": "John", "last_name": "Doe", "present": "no"},
        ])

        #replacement function to simulate user input
        def mock_input(p):
            if "Is John Doe present" in p:
                return "yes"
            return "no"
        
        #When
        students = mock_storage.read()
        for student in students:
            if mock_input(f"Is {student['first_name']} {student['last_name']} present? (yes/no): ").lower() == "yes":
                student["present"] = "yes"
            else:
                student["present"] = "no"
        
        mock_storage.write(students)

        #Then
        expected_data = [
            {"first_name": "John", "last_name": "Doe", "present": "yes"},
        ]
        assert mock_storage.read() == expected_data