import hashlib

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as index # pylint: disable=unused-import
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_POST

from jfu.http import upload_receive, UploadResponse

from .storage import storage
from .models import User, Document
from .forms import ProfileForm



def drive_storage(request):	
    return render(request, "falcon_app/drive_storage.html")

def users(request):
    userlist = User.objects.all()
    return render(request, 'falcon_app/users.html', {'userlist':userlist})

@login_required
def dashboard(request):
    return render(request, 'falcon_app/dashboard.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=User.objects.get(user_ptr_id=request.user.id))
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/profile')
        else:
            return render(request, 'profile.html', {'form':form, 'error':'Invalid data'})
    else:   
        form = ProfileForm(instance=User.objects.get(user_ptr_id=request.user.id))
        return render(request, 'falcon_app/profile.html', {'form':form})
   
@login_required
def drive(request):
    return render(request, 'falcon_app/drive.html')

@require_POST
def upload(request):
    uploaded_file = upload_receive( request )
    file_dict = {
        'name' : uploaded_file.name,
        'size' : uploaded_file.size,
    }


    current_user = User.objects.get(user_ptr_id=request.user.id)
    
    if current_user.balance_quota < uploaded_file.size:
        message = "Sorry insufficient storage"
        file_dict['name']= message
        
    else:
        hash_value = hashlib.sha1(uploaded_file.read()).hexdigest()
        
        doc = Document(file_name=uploaded_file.name,
                       file_size=uploaded_file.size,
                       file_type=uploaded_file.content_type,
                       hash_address=hash_value,
                       owner=current_user
       )
        doc.save()
    
        uploaded_file.seek(0)
        store_obj = storage.get_storage()
        obj = store_obj.open(hash_value, 'w')
        obj.write(uploaded_file.read())
        obj.close()
    
    return UploadResponse(request, file_dict )
       
