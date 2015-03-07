import gnupg
import logging

ROOT_LOG = 'ezi-store'

class Gpg(object):
    def __init__(self, configure={}):
        self._LOG = logging.getLogger("%s.%s" % (ROOT_LOG, self.__class__.__name__))
        self._gpg_config = dict(configure['gpg'])
        self._gpg_gpghome = self._gpg_config['gnupghome']
        self._gpg_key_type = self._gpg_config['key_type']
        self._gpg_key_length = self._gpg_config['key_length']
        self._gpg_expire_data = self._gpg_config['expire_date']
#        self._gpg_name_real = self._gpg_config['name_real']
        self._gpg_name_real = 'ezi_store_srv'
        self._gpg_name_comment = self._gpg_config['name_comment']
        self._gpg_name_email = self._gpg_config['name_email']

        self._gpg = gnupg.GPG(gnupghome=self._gpg_config['gnupghome'])
        self._input_data = self._gpg.gen_key_input(key_type=self._gpg_key_type, key_length=self._gpg_key_length, expire_date=self._gpg_expire_data, name_real=self._gpg_name_real, name_comment=self._gpg_name_comment, name_email=self._gpg_name_email)

    def gen_key(self):
        self._gpg.gen_key(self._input_data)

    def srv_pub_key_exist(self):
        keys = self._gpg.list_keys()
        if keys == []:
            self._LOG.info('Server public key doesn\'t exist')
            return None
        print keys
#        ret = True
#        if self._gpg.list_keys() == []:
#            self._LOG.info('Public key doesn\'t exist')
#            ret = False
#        if self._gpg.list_keys(True) == []:
#            self._LOG.info('Private key doesn\'t exist')
#            ret = False
#        return retr

#    def export_armored_srv_pub_key(self, keyid):
#        return self._gpg.export_keys(keyid)
#
#    def export_armored_srv_sec_key(self, keyid):
#        return self._gpg.export_keys(keyid, True)
