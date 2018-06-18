from . import db
from datetime import datetime
from flask import url_for


class Permission:
    MAINTENANCE = 0x01
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    mtc_users = db.relationship('MtcUser', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'MtcUser': (0x01, True),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __str__(self):
        return '<Role %s>' % self.name


class MtcUser(db.Model):  # maintenance
    __tablename__ = 'mtc_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    telephone = db.Column(db.String(11))
    location = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


# 设施类型
class FacilityType(db.Model):
    __tablename__ = 'facility_types'
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(64), unique=True)
    facilities = db.relationship('Facility', backref='types', lazy='dynamic')

    def __str__(self):
        return '<FacilityType %s>' % self.facility_name


# 具体设施
class Facility(db.Model):
    __tablename__ = 'facilities'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, unique=True)
    facility_type = db.Column(db.Integer, db.ForeignKey('facility_types.id'))
    city = db.Column(db.String(64))
    district = db.Column(db.String(64))
    location = db.Column(db.String(255))
    description = db.Column(db.String(128))
    location_new = db.Column(db.String(255))
    install_user = db.Column(db.Integer, db.ForeignKey('mtc_users.id'))
    facility_img = db.Column(db.String(128))
    status = db.Column(db.Boolean, default=False)
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)
    update_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_json(self):
        json_facility = {
            'url': url_for('api.get_facility', id=self.id, _external=True),
            'facility_id': self.facility_id,
            'install_user': self.install_user,
            'city': self.city,
        }
        return json_facility
