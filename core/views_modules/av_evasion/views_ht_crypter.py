from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from requests import Response

from core import views
from core.views import ht, config, renderMainPanel, saveFileOutput, Logger

# Create your views here.

# ht_crypter

def cryptFile(request):
    this_conf = config['ht_crypter_cryptFile']
    if len(request.FILES) != 0:
        if request.FILES['filename']:
            # Get file
            myfile = request.FILES['filename']

            # Get Crypter Module
            crypter = ht.getModule('ht_crypter')

            # Save the file
            filename, location, uploaded_file_url = saveFileOutput(myfile, "crypter", "av_evasion")
            
            # Compile Exe
            compile_exe = False
            if request.POST.get('compile_exe','')=='on':
                compile_exe = True

            tmp_new_file_name = filename.split('.')[0]
            if not '.' in tmp_new_file_name:
                tmp_new_file_name = '{name}.py'.format(name=tmp_new_file_name)
            new_file_name = os.path.join(location, tmp_new_file_name)

            drop_file_name = filename
            if not '.' in drop_file_name:
                drop_file_name = '{name}.{ext}'.format(name=drop_file_name, ext=filename.split('.')[1])

            iterate_count = 1

            if request.POST.get('iteratecount'):
                try:
                    iterate_count = int(request.POST.get('iteratecount'))
                    if iterate_count < 1:
                        iterate_count = 1
                except:
                    pass

            prime_length = 2
            if request.POST.get('prime_length'):
                try:
                    prime_length = int(request.POST.get('prime_length'))
                    if prime_length < 1:
                        prime_length = 2
                except:
                    pass

            is_last = False
            if iterate_count == 1:
                is_last = True

            crypted_file = crypter.crypt_file(filename=uploaded_file_url, new_file_name=new_file_name, drop_file_name=drop_file_name, prime_length=prime_length, iterate_count=iterate_count, is_last=is_last, compile_exe=compile_exe)

            if crypted_file:
                if os.path.isfile(crypted_file):
                    with open(crypted_file, 'rb') as fh:
                        if compile_exe:
                            new_file_name = '{name}.exe'.format(name=new_file_name.split('.')[0])
                        response = HttpResponse(fh.read(), content_type="application/{type}".format(type=new_file_name.split('.')[1]))
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(crypted_file)
                        return response
                        os.remove(uploaded_file_url)
                        os.remove(crypted_file)
            else:
                Logger.printMessage(message='cryptFile', description=this_conf['bad_saved'], is_error=True)
            return renderMainPanel(request=request)

    return renderMainPanel(request=request)


def convertToExe(request):
	stub_name = request.POST.get('stub_name')
	ht.getModule('ht_crypter').convertToExe( stub_name=stub_name )

def createStub(request):
	crypto_data_hex = request.POST.get('crypto_data_hex')
	public_key = request.POST.get('public_key')
	drop_file_name = request.POST.get('drop_file_name')
	save_name = request.POST.get('save_name')
	is_iterating = request.POST.get('is_iterating', False)
	is_last = request.POST.get('is_last', False)
	convert = request.POST.get('convert', False)
	result = ht.getModule('ht_crypter').createStub( crypto_data_hex=crypto_data_hex, public_key=public_key, drop_file_name=drop_file_name, save_name=save_name, is_iterating=is_iterating, is_last=is_last, convert=convert )
	return renderMainPanel(request=request, popup_text=result)
	
def crypt_file(request):
	filename = request.POST.get('filename')
	new_file_name = request.POST.get('new_file_name')
	drop_file_name = request.POST.get('drop_file_name', 'dropped.py')
	prime_length = request.POST.get('prime_length', 4)
	compile_exe = request.POST.get('compile_exe', False)
	is_iterating = request.POST.get('is_iterating', False)
	iterate_count = request.POST.get('iterate_count', 1)
	is_last = request.POST.get('is_last', False)
	result = ht.getModule('ht_crypter').crypt_file( filename=filename, new_file_name=new_file_name, drop_file_name=drop_file_name, prime_length=prime_length, compile_exe=compile_exe, is_iterating=is_iterating, iterate_count=iterate_count, is_last=is_last )
	return renderMainPanel(request=request, popup_text=result)
	