import click


def pw_prompt() -> str:
    msg = "VMのroot userのパスワードを入力してくだいさい"
    return click.prompt(msg, hide_input=True, confirmation_prompt=True)


def sshkey_prompt() -> str:
    msg = "VMに紐付けるsshkey名を入力してくだいさい"
    return click.prompt(msg, hide_input=True, confirmation_prompt=True)
