# Record of what needs to be done

1. Make sure that ssh-agent is running

    eval "$(ssh-agent -s)"       # expect it to say something like 'Agent pid 2310'

    ssh-add ~/.ssh/id_ed25519    # I guess this adds the private key to whatever the ssh-agent is managing

    ssh -T git@github.com        # Checks if ssh is set up


2. Useful git commands to check if it is set up correctly

    git remote -v                # Tells you the current remote assignments

    git remote set-url origin git@github.com:jlgokingco/jlg_taxtools.git     # Sets up git remote

    git config --global user.name jlgokingco

    git config --global user.email jlgokingco@gmail.com

    git branch -M main          # Sets up which branch to use. Normally just main

3. Useful git commands for regular usage

    git status

    git commit -m "comments" file

    git push origin main
