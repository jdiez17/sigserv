from sigserv.github import gh
from sigserv.util import looks_like_sig, verify_sig, recv_pubkey
from sigserv.config import config
from sigserv.templates import *

def process_pr(pr, issue, f):
    """
        Checks if the PR contains a signature file,
        and if it does, ensures that it's valid.

        Criteria for auto-merge: there must be only
        one file changed, and it must be a valid sig.
    """

    files = list(pr.iter_files())
    if len(files) != 1:
        return # No automatic action if there isn't only one.

    sig = looks_like_sig(files[0])
    if sig:
        keyid = None

        # Obtain key id from the filename.
        try:
            keyid = files[0].filename.split("_")[-1].replace(".sig", "")
        except:
            # Unable to extract key id from filename. Probably bad format.
            issue.create_comment(NO_KEY_ID)
            pr.close()

            return

        # Fetch this person's public key.
        recv_pubkey(keyid)

        # Attempt to verify the signature.
        if verify_sig(sig, f):
            issue.create_comment(VERIFY_OK)
            pr.merge("Added {0}'s signature.".format(keyid))

            return
        else:
            issue.create_comment(VERIFY_FAIL)
            pr.close()

            return
    else:
        print("File in PR {0} doesn't look like a signature.".format(pr.html_url))

def main():
    for repo in config['repos']:
        parts = repo['path'].split("/")
        ghrepo = gh.repository(*parts)

        count = 0
        for pr in ghrepo.iter_pulls(state="open"):
            issue = gh.issue(parts[0], parts[1], pr.number)
            process_pr(pr, issue, repo['file'])

            count += 1

        print("Processed", count, "PRs.")
