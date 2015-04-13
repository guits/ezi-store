import gnupg
import logging

ROOT_LOG = 'ezi-store'

class Gpg(object):
    def __init__(self, configuration={}):
        try:
            self._LOG = logging.getLogger("%s.%s" % (ROOT_LOG, self.__class__.__name__))
            self._gpg_config = dict(configuration['gpg'])
            self._gpg_gpghome = self._gpg_config['gnupghome']
            self._gpg_key_type = self._gpg_config['key_type']
            self._gpg_key_length = self._gpg_config['key_length']
            self._gpg_expire_data = self._gpg_config['expire_date']
            self._gpg_name_real = self._gpg_config['name_real']
            self._gpg_name_comment = self._gpg_config['name_comment']
            self._gpg_name_email = self._gpg_config['name_email']

            self._gpg = gnupg.GPG(gnupghome=self._gpg_config['gnupghome'])
            self._input_data = self._gpg.gen_key_input(key_type=self._gpg_key_type, key_length=self._gpg_key_length, expire_date=self._gpg_expire_data, name_real=self._gpg_name_real, name_comment=self._gpg_name_comment, name_email=self._gpg_name_email)
        except (KeyError, AttributeError) as err:
            print "Error with GPG initialization: %s" % err

    def gen_keys(self):
        key = self._gpg.gen_key(self._input_data)

#{'dummy': u'', 'keyid': u'6981BB47EFDDAE99', 'expires': u'1457590722', 'subkeys': [], 'length': u'4096', 'ownertrust': u'u', 'algo': u'1', 'fingerprint': u'B61DDBA1101F5374BB974BFF6981BB47EFDDAE99', 'date': u'1426054722', 'trust': u'u', 'type': u'pub', 'uids': [u'Ezi Store (ezi-store server key) <ezi-store@zigzag.sx>']}

    def list_keys(self):
        keys = self._gpg.list_keys()
        tmp_keys = self._gpg.list_keys(True)
        for key in tmp_keys:
            keys.append(key)
        if keys == []:
            self._LOG.debug('No key found')
            return None
        for key in keys:
            print "--------------------------------------------------------------"
            for k, v in key.iteritems():
                if (v != 'u') and (k != 'uids') and (v != ''):
                    print "%s:\t%s" % (k, v)
                if k == 'uids':
                    print "uids:"
                    for uid in v:
                        print "\t%s" % (uid)
        print "--------------------------------------------------------------"

    def remove_keys(self, fingerprint):
        self._gpg.delete_keys(fingerprint, True)
        self._gpg.delete_keys(fingerprint)

    def export_armored_pub_key(self, keyid):
        return self._gpg.export_keys(keyid)

    def export_armored_sec_key(self, keyid):
        return self._gpg.export_keys(keyid, True)

    def import_keys(self, data):
        self._gpg.import_keys(data)
