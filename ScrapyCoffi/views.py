from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.

from ldap3 import Server, Connection, ALL, Tls
import ssl

#@login_required


@login_required(login_url='login')
def homeView(request):
    valor=None
    micontexto = {'user': request.user}
    if request.method == 'POST':
        usuario = request.POST['elusuario']
        #usuario='fcabrera'
        if usuario:
            tls_configuration = Tls( validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1 )
            tls_configuration.validate = ssl.CERT_NONE
            server = Server( 'ldaps://172.24.3.3:636', use_ssl=True, tls=tls_configuration )
            conn = Connection( server, 'cn=dcoffi,ou=dtsc,ou=admin,ou=ccs,o=bcv', 'password', auto_bind=True )
            conn.search('O=BCV', '(fullname=' + usuario + '*)',
                        attributes=['fullName', 'telephoneNumber', 'title', 'workforceID', 'l', 'mail', 'ou',
                                    'passwordExpirationTime','cn','nGWGroupWiseID'])
            valor = conn.entries
            micontexto.update({'resultados': valor,'post':True})
    return render(request=request, context=micontexto, template_name='home.html')






