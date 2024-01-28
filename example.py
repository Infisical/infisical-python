from infisical import InfisicalClient

OLD_SERVICE_TOKEN = "TOKEN"

client = InfisicalClient(
    site_url="http://localhost:8080",
    token=OLD_SERVICE_TOKEN,
    debug=True
    )

def random_string(length: int):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters) for _i in range(length))




secrets = client.get_all_secrets(environment="dev")
for secret in secrets:
    print(secret.secret_name, " : ", secret.secret_value)


test_secret = client.get_secret(secret_name="TEST_SECRET", environment="dev", type="shared")
print("TEST SECRET VALUE: ", test_secret.secret_value)


create_secret = client.create_secret(secret_name=random_string(12), secret_value=random_string(12), environment="dev")
print("CREATED SECRET: ", create_secret.secret_name, " : ", create_secret.secret_value)

updated_secret = client.update_secret(secret_name=create_secret.secret_name, secret_value=random_string(12), environment="dev")
print("UPDATED SECRET: ", updated_secret.secret_name, " : ", updated_secret.secret_value)

delete_secret = client.delete_secret(secret_name=updated_secret.secret_name, environment="dev")
print("DELETED SECRET: ", delete_secret.secret_name, " : ", delete_secret.secret_value)