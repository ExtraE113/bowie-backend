# Backend Code for [Bowie](https://github.com/ExtraE113/bowie)

Bowie is a single-tap mobile donation application for the [Alemeda County Community Food Bank](https://accfb.org).

## Installation

1. Clone the project

2. Run `pip3 install -r requirements.txt` to install dependencies

3. For local testing, set the following environment variables. Either set them to your own values or, for trusted contributors, contact [ExtraE113](https://github.com/ExtraE113) for the information.

|Variable | Value |
|---------|-------|
|`GOOGLE_APPLICATION_CREDENTIALS`| Path to the firebase admin SDK credentials (`.json`). |
|`SQUARE_APPLICATION_ID`| The square application id. Can be accessed from the square developer dashboard. Should be the sandbox id because production deployments should use the secret manager for GCP.|
|`SQUARE_APPLICATION_TOKEN`| Above, but the token instead of the ID. |
|`BOWIE_BACKEND_DEBUG`| Set to any non-empty string in local testing or debug environments, although it is good form to set to `True`. Should not be set in production.|



## Running the code
For testing, use functions-framework (installed with pip from requirements above)
```bash
functions-framework --target=endpoint --debug
```
Where `endpoint` is the endpoint you'd like to test. More information about `functions-framework` [here.](https://github.com/GoogleCloudPlatform/functions-framework-python)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests (such as they exist) as appropriate. All new features should have tests.

Remember to include any new packages with `pip freeze > requirements.txt`
## License
[GNU Affero General Public License](https://choosealicense.com/licenses/agpl-3.0/)

## Questions
Contact [ExtraE113](https://github.com/ExtraE113) with any questions, or open an issue.