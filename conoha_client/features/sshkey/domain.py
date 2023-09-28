"""sshkey Domain Objects."""


from pydantic import BaseModel


class KeyPair(BaseModel):
    """os-keypairs API Response Unit."""

    public_key: str
    name: str
    fingerprint: str
