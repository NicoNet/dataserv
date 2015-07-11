from dataserv.run import db

class Audit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer)

    audit_seed = db.Column(db.String(128))
    audit_response = db.Column(db.String(128))

    def __init__(self, contract_id, audit_seed, audit_response):
        self.contract_id = contract_id

        self.audit_seed = audit_seed
        self.audit_response = audit_response

        self.save()

    def complete_audit(self, response):
        """Complete the audit, and delete if completed."""
        if response == self.audit_response:
            self.delete()
            return True
        return False

    def save(self):
        """Save the audit to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Remove audit from the database."""
        db.session.delete(self)
        db.session.commit()
