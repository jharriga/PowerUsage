# Required EDITS to pwr_playbook.yaml
## MUST EDIT TO ADD LOGIN CREDENTIALS at lines 51 and 94
## ENSURE THAT PATH TO {pwr_script} line 92 IS VALID

# Sample Usage
ansible-playbook -e "rf=10.26.9.132 sut=10.26.9.131 runtime=120 interval=5 numpar=64" pwr_playbook.yml

> Creates '<numpar>_test.log output file
