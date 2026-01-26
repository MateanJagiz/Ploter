#!/bin/fish

eval (ssh-agent -c)

ssh-add ~/.ssh/id_ed25519_github

ssh -T git@github.com

