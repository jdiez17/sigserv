import requests
import gnupg
import io

gpg = gnupg.GPG()

def looks_like_sig(f):
    downloaded = requests.get(f.raw_url)

    # Pretty crude, but it'll do for now
    if "-----BEGIN PGP SIGNATURE-----" in downloaded.text:
        return downloaded.text

    return False

def verify_sig(sig, path):
    # TODO: Had to modify verify_file, submit pr

    v = gpg.verify_file(io.StringIO(sig), path)
    return v.trust_level is not None

def recv_pubkey(keyid):
    return gpg.recv_keys(keyid)
