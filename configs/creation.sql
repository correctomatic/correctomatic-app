--------------------------------------------------
-- Aules ED
--------------------------------------------------
INSERT INTO platform (id, url, client_id, auth_login_url, auth_token_url, auth_audience, key_set_url, private_key_file, public_key_file, "default")
VALUES
  (
    1,
    'https://aules.edu.gva.es/ed',
    'YD56yxE8ywXKrjt',
    'https://aules.edu.gva.es/ed/mod/lti/auth.php',
    'https://aules.edu.gva.es/ed/mod/lti/token.php',
    NULL,
    'https://aules.edu.gva.es/ed/mod/lti/certs.php',
    'private.key',
    'public.key',
    true
  );

-- Deployments
INSERT INTO deployment (platform_id, deployment_id)
VALUES
  (1, '3');



--------------------------------------------------
-- Aules Docent
--------------------------------------------------
INSERT INTO platform (id, url, client_id, auth_login_url, auth_token_url, auth_audience, key_set_url, private_key_file, public_key_file, "default")
VALUES
  (
    2,
    'https://aules.edu.gva.es/docent',
    'rFQZfRCMVipPH6v',
    'https://aules.edu.gva.es/docent/mod/lti/auth.php',
    'https://aules.edu.gva.es/docent/mod/lti/token.php',
    NULL,
    'https://aules.edu.gva.es/docent/mod/lti/certs.php',
    'private.key',
    'public.key',
    true
  );

-- Deployments
INSERT INTO deployment (platform_id, deployment_id)
VALUES
  (2, '169');



--------------------------------------------------
-- Local, http://moodle.lti
--------------------------------------------------
INSERT INTO platform (id, url, client_id, auth_login_url, auth_token_url, auth_audience, key_set_url, private_key_file, public_key_file, "default")
VALUES
  (
    3,
    'http://moodle.lti',
    'VeDBJjVL0qiEB6z',
    'http://moodle.lti/mod/lti/auth.php',
    'http://moodle.lti/mod/lti/token.php',
    NULL,
    'http://moodle.lti/mod/lti/certs.php',
    'private.key',
    'public.key',
    true
  );

-- Deployments
INSERT INTO deployment (platform_id, deployment_id)
VALUES
  (3, '1'),
  (3, '2');
