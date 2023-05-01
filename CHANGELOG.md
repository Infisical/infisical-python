# Changelog

All notable changes will be documented in this file.

## [1.2.0] - 2023-05-01

Patched `expires_at` on `GetServiceTokenDetailsResponse` to be optional (to accomodate for cases where the service token never expires).

## [1.1.0] - 2023-04-27

This version adds support for querying and mutating secrets by name with the introduction of blind-indexing. It also adds support for caching by passing in `cache_ttl`.

- `get_all_secrets()`: Method to get all secrets from a project and environment
- `create_secret()`: Method to create a secret
- `get_secret()`: Method to get a secret by name
- `update_secret()`: Method to update a secret by name
- `delete_secret()`: Method to delete a secret by name

The format of any fetched secrets from the SDK is now a `SecretBundle` that has useful properties like `secret_name`, `secret_value`, and `version`.

This version also deprecates the `connect()` and `create_connection()` methods in favor of initializing the SDK with `new InfisicalClient(options)`

It also includes some tests that can be run by passing in a `INFISICAL_TOKEN` and `SITE_URL` as environment variables to point the test client to an instance of Infisical.