from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from ldap3 import Server, Connection, ALL, Tls
import ssl
from django.contrib.auth import authenticate, login

@login_required
def mostrarusuarioldap(request):
    usuario="francys"
    tls_configuration = Tls( validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1 )
    tls_configuration.validate = ssl.CERT_NONE
    server = Server( 'ldaps://172.24.3.3:636', use_ssl=True, tls=tls_configuration )
    conn = Connection( server, 'contexto', 'password', auto_bind=True )
    conn.search( 'O=BCV', '(fullname=' + usuario + '*)',
                 attributes=['fullName', 'telephoneNumber', 'title', 'workforceID', 'l', 'mail', 'ou',
                             'passwordExpirationTime'] )
    valor = conn.entries
    ctx={'usuarios' : valor}
    return render(request=request, context=ctx, template_name='usuarios.html')


@login_required(login_url='login')
def homeView(request):
    return render(request=request, context={'user': request.user}, template_name='home.html')
