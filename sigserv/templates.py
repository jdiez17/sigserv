VERIFY_OK = """
Thanks! :thumbsup:"""

VERIFY_FAIL = """
Sorry, I was unable to verify your signature.
Check that your public key is available from a public key server and that you have signed the file correctly according to [SIGNING.md](SIGNING.md)
"""

NO_KEY_ID = """
I was unable to extract the key ID from your file name. You probably didn't name your signature correctly, so please review (thing)[] and submit another PR."""
