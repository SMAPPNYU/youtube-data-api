# How to Test Youtube-Data-API
[Michael Liu](Michael98Liu) 2018-11-01
## Environment Setup
### API Key
To use YouTube Data API, you need to obtain a API key and register your application on [Google Developer Console](https://developers.google.com/youtube/v3/getting-started). After obtaining the key, you should add `export YT_KEY="[your API key]"` to your bash configuration file, which is `~/.bash_profile` if you are testing this API on a MacOS. To see if you have successfully set the environment variable, run `echo $YT_KEY`, and you should see your key printed out in the terminal. In this way, your API key is private to yourself, and never exposed to other developers.

### Library Dependencies
There are also several library dependencies of this API. To install them, run command `pip install -r requirements.txt`. If you encounter any problems when setting up your environment, please raise an issue on the [issue page](https://github.com/SMAPPNYU/youtube-data-api/issues?q=is%3Aopen+is%3Aissue).

## Test Locally
### Python Unittest
We use `unittest` library to test our software. The essentialism idea of this framework is firstly, to execute your code, and secondly, to run a series of assertions on the return values of your functions, and to check if all of them are same as the predetermined value. Therefore, you could test your code in three different ways:
1. check if classes/functions execute without throwing exceptions,
2. check if the execution handling procedures are error-free, and
3. check if the data collected by the API is the one you want.

Tests are implemented as classes that inherit from `TestCase` class. Each class normally consist a `setUp` method that is executed before executing every test, or a `setUpClass` method that is called once before executing You can write however many methods you like to test. A test method is simply a class method that contains a bunch of assertions. For example, this is how we test if the function to verify API key is returning the correct response.

```python
class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)

    @patch('requests.get')
    def test_verify(self, mock_request):
        mock_resp = requests.models.Response()
        mock_resp.status_code = 404
        mock_request.return_value = mock_resp

        self.assertEqual(self.yt.verify_key(), False)
```

For more technical details, please refer to the [documentation](https://docs.python.org/3/library/unittest.html) of unittest.

### Running the tests
In the test cases provided by us, we arrange test files by different functions we are trying to test. For the cases where we need to check the validity of data returned by the API call, we provide a bunch of manually collected data that are stored in `./tests/data`, all as json files.

To run a single unittest case, run command `python -m unittest [test_file]`. However, since we have multiple test cases, we aggregate all the test command into makefile. Now, to run the test, simply run command `make test`. You will see in the command line output which files are tested, whether the code throws out any exceptions, and how many test cases have passed. In this way, we also facilitates test on Travis.

## Using Travis
[Travis](https://travis-ci.com/) is a continuous integration platform that allows you to build and test your code automatically, and provides you with instant feedback. In the main readme doc of this API, you could see a badge that looks like <a href="https://travis-ci.com/SMAPPNYU/youtube-data-api"><img src="https://travis-ci.com/SMAPPNYU/youtube-data-api.svg?branch=master" alt="Build status" height="18"></a>, that shows you wether the software is successfully built or not.

We specify how we would like our code to be tested in the `.travis.yml` file. For example, we specified that this API is written in Python 3.6, and what libraries are required to build. Notice that the `script` filed is where you specify how the code are gonna be tested, in our case, the command `make test`. Also remember that you need to add the `TY_KEY` environment variable in the [settings page](https://travis-ci.com/SMAPPNYU/youtube-data-api/settings) of Youtube Data API travis page. After you are all set, click "Restart Build" on the page, and, lo and behold, travis will tell you whether your code is bug-free.

![API Key](https://i.imgur.com/QpLqdbd.png)

## Add More Tests
Standing by the philosophy of [continuous integration (CI)](https://docs.travis-ci.com/user/for-beginners/#what-is-continuous-integration-ci), we warmly welcome more tests from the open source community, as well as the SMAPP lab members at New York University. Your contributions are invaluable to us. Several things to notice were you to add more tests:
1. If you need more data in order to check the validity of certain API call, please manually collect them and store as json files in `./tests/data` directory.
2. As I have mentioned before, tests are arranged so that each file only tests a specific function of the API. New test cases on existing functions should go to the corresponding test files. You are free to create new files to test new functions that were either missed before or newly created.
3. When you add new test cases, don't forget to add `python -m unittest [new_test_file]` command to [../makefile](https://github.com/SMAPPNYU/youtube-data-api/blob/master/Makefile)`. **Be sure each test case is tab separated!**
4. Create a NEW branch before committing any changes.
