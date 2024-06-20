python -m venv .venv
pip install flask psycopg2-binary
pip install debugpy python-dotenv


**Super Interesting**:
https://pypi.org/project/PyLTI1p3/

## Run the app in development mode
Very important: listen on all hosts, so correctomatic notifier can access this app:

```bash
flask run --debugger --reload --host=0.0.0.0
```

- `.env` contents are loaded automatically by Flask when the app is run in development mode.
- You can open a shell with the app context by running `flask shell`.



Interesant things to check:
- [Custom commands](https://flask.palletsprojects.com/en/3.0.x/cli/#custom-commands)

```sh
flask shell

from app import create_app
app = create_app()
app.url_map
```


The fields in an LTI 1.3 launch request contain various pieces of information required for the successful launching of an LTI-compliant tool from a Learning Management System (LMS). Here's an explanation of each field in the given JSON object:

1. **nonce**: A unique value to ensure that the request is not a replay attack. It should be used only once.

2. **iat** (Issued At): The timestamp indicating when the token was issued, in seconds since the Unix epoch.

3. **exp** (Expiration): The timestamp indicating when the token will expire, in seconds since the Unix epoch.

4. **iss** (Issuer): The issuer of the token, which in this case is the LMS (`http://moodle.lti`).

5. **aud** (Audience): The intended recipient of the token, typically the client ID of the tool provider (`ZHD2HCuDCNrSEkG`).

6. **https://purl.imsglobal.org/spec/lti/claim/deployment_id**: The unique identifier for the deployment within the LMS (`2`).

7. **https://purl.imsglobal.org/spec/lti/claim/target_link_uri**: The URL where the tool should be launched (`http://app.host.lti:5000/launch`).

8. **sub**: The subject of the token, typically the unique identifier for the user within the LMS (`2`).

9. **https://purl.imsglobal.org/spec/lti/claim/lis**: Information related to the Learning Information Services (LIS):
    - **person_sourcedid**: The sourced identifier for the person (empty in this case).
    - **course_section_sourcedid**: The sourced identifier for the course section (empty in this case).

10. **https://purl.imsglobal.org/spec/lti/claim/roles**: The roles of the user within the context of the LMS:
    - `http://purl.imsglobal.org/vocab/lis/v2/institution/person#Administrator`: Institution-level administrator.
    - `http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor`: Instructor in the course.
    - `http://purl.imsglobal.org/vocab/lis/v2/system/person#Administrator`: System-level administrator.

11. **https://purl.imsglobal.org/spec/lti/claim/context**: Contextual information about the course:
    - **id**: The unique identifier for the course (`2`).
    - **label**: A short label for the course (`cursopruebas`).
    - **title**: The full title of the course (`Curso de pruebas`).
    - **type**: The type of context (not fully listed here).

12. **https://purl.imsglobal.org/spec/lti/claim/resource_link**: Information about the resource link being launched:
    - **title**: The title of the resource link (`Prueba LTI`).
    - **description**: A description of the resource link (empty).
    - **id**: The unique identifier for the resource link (`2`).

13. **https://purl.imsglobal.org/spec/lti-bo/claim/basicoutcome**: Information for basic outcomes:
    - **lis_result_sourcedid**: A unique identifier for the result, including instance ID, user ID, type ID, and launch ID, along with a hash for verification.
    - **lis_outcome_service_url**: The URL to the service endpoint where outcomes can be reported (`http://moodle.lti/mod/lti/service.php`).

14. **given_name**: The given name of the user (`Admin`).

15. **family_name**: The family name of the user (`Adminsurname`).

16. **name**: The full name of the user (`Admin Adminsurname`).

17. **https://purl.imsglobal.org/spec/lti/claim/ext**: Additional information:
    - **user_username**: The username of the user (`admin`).
    - **lms**: The LMS name and version (`moodle-2`).

18. **email**: The email address of the user (`spam1@gammu.com`).

19. **https://purl.imsglobal.org/spec/lti/claim/launch_presentation**: Presentation information for the launch:
    - **locale**: The locale of the user (`en`).
    - **document_target**: How the content should be displayed (`iframe`).
    - **return_url**: The URL to return to after the launch (`http://moodle.lti/mod/lti/return.php?course=2&launch_container=3&instanceid=2&sesskey=jXyERUUMWo`).

20. **https://purl.imsglobal.org/spec/lti/claim/tool_platform**: Information about the tool platform:
    - **product_family_code**: The product family code of the LMS (`moodle`).
    - **version**: The version of the LMS (`2021051718`).
    - **guid**: A unique identifier for the platform instance (`moodle.lti`).
    - **name**: The name of the platform (`cursodepruebas`).
    - **description**: A description of the platform (`Curso de pruebas`).

21. **https://purl.imsglobal.org/spec/lti/claim/version**: The version of the LTI specification being used (`1.3.0`).

22. **https://purl.imsglobal.org/spec/lti/claim/message_type**: The type of LTI message (`LtiResourceLinkRequest`).

These fields collectively provide the necessary context, user information, and security details required for an LTI tool to process the launch request and present the appropriate content to the user.
