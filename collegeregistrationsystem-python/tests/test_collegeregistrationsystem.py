import unittest

from src.collegeregistrationsystem import CollegeRegistrationSystem
from src.coursealreadyexistsexception import CourseAlreadyExistsException
from src.coursenotfoundexception import CourseNotFoundException
from src.collegemember import CollegeMember

from tests.constants import STUDENT_FIRST_ID
from tests.constants import STUDENT_1_FIRSTNAME_VALID
from tests.constants import STUDENT_1_LASTNAME_VALID
from tests.constants import STUDENT_1_DATEOFBIRTH_VALID
from tests.constants import STUDENT_1_EMAILADDRESS_VALID
from tests.constants import STUDENT_1_HOMEADDRESS_VALID
from tests.constants import STUDENT_1_HOMEADDRESS_INVALID

from tests.constants import COURSE_1_TITLE
from tests.constants import COURSE_1_NUMBEROFCREDITS_VALID
from tests.constants import COURSE_1_NUMBEROFCREDITS_INVALID

from tests.constants import COURSE_1_COURSESECTION_1_ENROLLMENTCAP_VALID
from tests.constants import COURSE_1_COURSESECTION_1_ENROLLMENTCAP_INVALID

class CollegeRegistrationSystemTest(unittest.TestCase):
    college_registration_system = None

    def setUp(self):
        self.college_registration_system = CollegeRegistrationSystem()
        return super().setUp()
    
    def tearDown(self):
        self.college_registration_system = None
        return super().tearDown()

    def test_add_student_violates_preconditions(self):
        # Call the unit under test
        with self.assertRaises(TypeError):
            self.college_registration_system.add_student(STUDENT_1_FIRSTNAME_VALID, STUDENT_1_LASTNAME_VALID, STUDENT_1_DATEOFBIRTH_VALID, STUDENT_1_EMAILADDRESS_VALID, STUDENT_1_HOMEADDRESS_INVALID)
        # Check the post-conditions
        # 
		# With an invalid home address, should raise TypeError (See with statement above)

    def add_student_succeeds_helper(self):
        # Call the unit under test
        try:
            student1 = self.college_registration_system.add_student(STUDENT_1_FIRSTNAME_VALID, STUDENT_1_LASTNAME_VALID, STUDENT_1_DATEOFBIRTH_VALID, STUDENT_1_EMAILADDRESS_VALID, STUDENT_1_HOMEADDRESS_VALID)
            # Check the post-conditions
            self.assertIsNotNone(student1)
            self.assertEqual(student1.get_id(), STUDENT_FIRST_ID)
            self.assertEqual(student1.get_first_name(), STUDENT_1_FIRSTNAME_VALID)
            self.assertEqual(student1.get_last_name(), STUDENT_1_LASTNAME_VALID)
            self.assertEqual(student1.get_email_address(), STUDENT_1_EMAILADDRESS_VALID)
            self.assertEqual(student1.get_date_of_birth(), STUDENT_1_DATEOFBIRTH_VALID)
            self.assertEqual(student1.get_home_address(), STUDENT_1_HOMEADDRESS_VALID)
            # Check the student is the only college member
            college_member_listing = self.college_registration_system.get_college_member_listing()
            self.assertEqual(len(college_member_listing), 1)
            self.assertEqual(college_member_listing[0], student1)
            return student1
        except TypeError:
            # The setup ensured the input parameters are valid.
            self.fail()
            return None
        
    def test_add_student_satisfies_preconditions(self):
        self.add_student_succeeds_helper()

    def test_get_college_member_succeeds(self):
        # Add a student.
        student1 = self.college_registration_system.add_student(STUDENT_1_FIRSTNAME_VALID, STUDENT_1_LASTNAME_VALID, STUDENT_1_DATEOFBIRTH_VALID, STUDENT_1_EMAILADDRESS_VALID, STUDENT_1_HOMEADDRESS_VALID)

        # Attempt to get the student.
        student1pointer: CollegeMember = self.college_registration_system.get_college_member(student1.get_id())

        # Try getting the student info.
        try:
            self.assertIsNotNone(student1pointer)
            self.assertEqual(student1pointer.get_id(), STUDENT_FIRST_ID)
            self.assertEqual(student1pointer.get_first_name(), STUDENT_1_FIRSTNAME_VALID)
            self.assertEqual(student1pointer.get_last_name(), STUDENT_1_LASTNAME_VALID)
            self.assertEqual(student1pointer.get_email_address(), STUDENT_1_EMAILADDRESS_VALID)
            # I don't know what else to add.
            return student1pointer
        except TypeError:
            # If this error was raised, then the get_college_menber() function did not work correctly.
            self.fail()
            return None
            


    def test_get_college_member_reports_collegemembernotfound(self):
        # TODO
        self.fail("Not implemented yet.")

    def test_add_course_violates_preconditions(self):
		# Call the unit under test
        with self.assertRaises(TypeError):
            try:
                self.college_registration_system.add_course(COURSE_1_TITLE, COURSE_1_NUMBEROFCREDITS_INVALID)
                # Check the post-conditions 
		        # 
		        # With an invalid number of credits, should raise TypeError (See with statement)
            except CourseAlreadyExistsException:
                # Since there is not already a course with this title,
		        # this exception should not be raised.
                self.fail()

    def add_course_succeeds_helper(self):
        try:
            # Call the unit under test
            course1 = self.college_registration_system.add_course(COURSE_1_TITLE, COURSE_1_NUMBEROFCREDITS_VALID)
		    # Check the post-conditions
		    #
		    # Check the class fields
            self.assertIsNotNone(course1)
            self.assertEqual(course1.get_title(), COURSE_1_TITLE)
            self.assertEqual(course1.get_number_of_credits(), COURSE_1_NUMBEROFCREDITS_VALID)
		    # Check that the Course is in only one in the CourseRegistry
            course_listing = self.college_registration_system.get_course_listing()
            self.assertEqual(len(course_listing), 1)
            self.assertEqual(course_listing[0], course1)
            return course1
        except CourseAlreadyExistsException:
            # Since there is not already a course with this title,
		    # this exception should not be raised.
            self.fail()
            return None
        except TypeError:
            # The setup ensured the input parameteters are valid.
            self.fail()
            return None
        
    def test_add_course_satisifies_preconditions(self):
        self.add_course_succeeds_helper()

    def test_add_course_reports_coursealreadyexists(self):
        # Perform set up and check pre-conditions
        self.add_course_succeeds_helper()
        # Call the unit under test
        with self.assertRaises(CourseAlreadyExistsException):
            try:
                self.college_registration_system.add_course(COURSE_1_TITLE, COURSE_1_NUMBEROFCREDITS_VALID)
                # Check the post-conditions 
		        # 
		        # Since the setup already added a course with the same title,
		        # should raise CourseAlreadyExistsException (See with statement)
            except TypeError:
                # The setup ensured the input parameters are valid.
                self.fail()

    def test_get_course_succeeds(self):
        # Perform setup and check pre-conditions
        course1 = self.add_course_succeeds_helper()
        # Call the unit under test
        try:
            course_found = self.college_registration_system.get_course(course1.get_id())
            # Check the post-conditions
            self.assertEqual(course1, course_found)
        except CourseNotFoundException:
            # The setup ensured that course1 does exist in the CourseRegistry.
            self.fail()

    def test_get_course_reports_coursenotfound(self):
        # Perform setup and check pre-conditions
        #
        # There are no courses.
        self.assertEqual(len(self.college_registration_system.get_course_listing()), 0)
        # Call the unit under test
        with self.assertRaises(CourseNotFoundException):
            self.college_registration_system.get_course(1)
        # Check the post-conditions
        #
        # When there are no courses, should raise CourseNotFoundException (See with statement)

    def test_add_course_section_violates_preconditions(self):
        # Perform the setup and check the pre-conditions
        course1 = self.add_course_succeeds_helper()
        # Call the unit under test
        with self.assertRaises(TypeError):
            try:
                self.college_registration_system.add_course_section(course1.get_id(), COURSE_1_COURSESECTION_1_ENROLLMENTCAP_INVALID)
                # Check the post-conditions
                #
                # Since the enrollment cap is not a non-negative number,
                # should raise TypeError (See with statement)
            except CourseNotFoundException:
                # The setup ensured that course1 does exist
                # in the CourseRegistry.
                self.fail()

    def add_course_section_succeeds_helper(self):
        # Peform the setup and check the pre-conditions
        course1 = self.add_course_succeeds_helper()
        # Call the unit under test
        try:
            course_section1 = self.college_registration_system.add_course_section(course1.get_id(), COURSE_1_COURSESECTION_1_ENROLLMENTCAP_VALID)
            # Check the post-conditions
            self.assertIsNotNone(course_section1)
            self.assertEqual(course_section1.get_course(), course1)
            self.assertEqual(course_section1.get_section_number(), 1)
            self.assertEqual(course_section1.get_enrollment_cap(), COURSE_1_COURSESECTION_1_ENROLLMENTCAP_VALID)
            # A faculty has not been assigned to teach the course section yet
            self.assertIsNone(course_section1.get_assigned_faculty())
            # There are no students enrolled in the course section yet
            self.assertEqual(len(course_section1.get_enrolled_students_listing()), 0)
            # Check that the course only has the one course section.
            course_section_listing = course1.get_course_section_listing()
            self.assertEqual(len(course_section_listing), 1)
            self.assertEqual(course_section_listing[0], course_section1)
            return course_section1
        except CourseNotFoundException:
            # The setup ensured that course1 does exist in the CourseRegistry.
            self.fail()
            return None
        except TypeError:
            # The setup ensured the input parameters are valid.
            self.fail()
            return None       

    def test_add_course_section_satisfies_preconditions(self):
        self.add_course_section_succeeds_helper()

    def test_enroll_returns_true(self):
        # TODO
        self.fail("Not implemented yet.")
	
    def test_enroll_returns_false(self):
        # TODO
        self.fail("Not implemented yet.")
            
    def test_drop_returns_true(self):
        # TODO
        self.fail("Not implemented yet.")

    def test_drop_returns_false(self):
        # TODO
        self.fail("Not implemented yet.")
