# tests to ensure testing framework has been setup properly

from .FakeClass import make_fake_message, run

def test_tests():
    _test_test()
    _test_help_command()

def _test_test():
    # test to ensure testing framework is running
    assert True

def log(message):
    with open('./test.log', 'a+') as file:
        file.write(message + '\n')

def _test_help_command():
    help_command = make_fake_message("fs.help")
    channel = run(help_command)
    log(channel.get_contents())