import gnupg
import logging

class Gpg(object):
    def __init__(self, configuration={}):
        try:
            self._LOG = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))
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

    def encode(self, data, keyid):
        encoded = self._gpg.encrypt(data=data, recipients=keyid, always_trust=True)
        return encoded

    def decode(self, data, keyid):
        decoded = self._gpg.decrypt(data, always_trust=True)
        return decoded
