from dataserv.run import db
from dataserv.Validator import is_btc_address, is_sha256


class Audit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    btc_addr = db.Column(db.String(35))

    audit_block = db.Column(db.Integer)
    audit_seed = db.Column(db.String(128))
    audit_response = db.Column(db.String(128))

    def __init__(self, btc_addr, audit_seed, audit_block, audit_response):
        self.btc_addr = btc_addr

        self.audit_seed = audit_seed
        self.audit_block = audit_block
        self.audit_response = audit_response

        self.validate()
        self.save()

    def save(self):
        """Save the audit to the database."""
        db.session.add(self)
        db.session.commit()

    def validate(self):
        """Validate the object."""
        if not is_btc_address(self.btc_addr):
            raise ValueError("Invalid Bitcoin Address.")
        if not is_sha256(self.audit_seed):
            raise ValueError("Invalid Seed.")
        if not is_sha256(self.audit_response):
            raise ValueError("Invalid Response.")
