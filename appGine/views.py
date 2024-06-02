from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .form import FormUser,Formdatauser,FormPost
from .models import DataUser,BlockPost,CommentPost

# Create your views here.
def mainPage(request):
    return render(request,'main_page.html')

def aboutPage(request):
    return render(request,'about_page.html')

def requestPage(request):
    return render(request,'request_page.html')

def signupPage(request):  ## Sign Up
    if request.method == 'POST':
        Username = request.POST['username-signup']
        Email = request.POST['email-signup']
        Password = request.POST['password-signup']
        Password2 = request.POST['confirm-signup']
        field = ['username','email','password','confirm password']
        count = 0
        check = [Username,Email,Password,Password2]
        name = ['username-signup','email-signup','password-signup','confirm-signup']
        if Password != Password2 and Password != '' and Password2 != '':
            message = messages.error(request,f'Password not match with {field[3]}.') ; del message
            del Username,Email,Password,Password2,check,field,count
            return render(request,'signup_page.html',{'name':name[2]})
        else:
            pass
        for i in check:
            if i == '':
                message = messages.error(request,f'Field {field[count]} is empty.') ; del message
                del Username,Email,Password,Password2,check,field
                return render(request,'signup_page.html',{'name':name[count]})
            else:
                count += 1
        for j,k in User.objects.all().values_list('username','email'):
            if j == Username:
                message = messages.error(request,'This username is already used.') ; del message
                del Username,Email,Password,Password2,check,field,count
                return render(request,'signup_page.html',{'name':name[0]})
            if k == Email:
                message = messages.error(request,'This email is already used.') ; del message
                del Username,Email,Password,Password2,check,field,count
                return render(request,'signup_page.html',{'name':name[1]})
            else:
                pass
        users = User.objects.create_user(username=Username,password=Password,email=Email)
        users.save()
        data_user = DataUser(user=users)
        data_user.save()
        del Username,Email,Password,Password2,check,field,count,name,data_user,users
        return redirect('login')
    else:
        return render(request,'signup_page.html')

def loginPage(request): ## Login Gine
    if request.method == 'POST':
        username = request.POST['username-login']
        password = request.POST['password-login']
        user = authenticate(request=request,username=username,password=password)
        if user is not None:
            login(request=request,user=user)
            del password,user,username
            return redirect('profile')
        else:
            del username,password,user
            message = messages.error(request,'Please check username or password.') ; del message
            return redirect('login')
    else:
        return render(request,'login_page.html')

@login_required(login_url='login')
def profilePage(request):  ## Profile User
    if request.method == 'POST':
        if request.POST.get('save-profile') is not None: ## update Data User
            update = User.objects.get(id=request.user.id)
            update.first_name = request.POST['first_name']
            update.last_name = request.POST['last_name']
            update.email = request.POST['email']
            update.save()
            data = DataUser.objects.get(user = request.user.id)
            if request.FILES.get('picture') is not None:
                if data.picture.url == '/media/media/user.png':
                    pass
                else:
                    data.picture.delete()
                data.picture = request.FILES['picture']
            else:
                pass
            data.birthday = request.POST['birthday']
            data.location = request.POST['location']
            data.birthday = request.POST['birthday']
            data.sex = request.POST['sex']
            data.phone = request.POST['phone']
            data.bio = request.POST['bio']
            data.save()
            del data,update
            messages.success(request,'Profile Update Successfully')
            return redirect('profile')
        if request.POST.get('logout-profile') is not None: ## Logout
            logout(request=request)
            return redirect('login')
        if request.POST.get('btn-createblock') is not None:  ## Create Block Post
            user_ = User.objects.get(username=request.user)
            formpost = FormPost(request.POST)
            if formpost.is_valid():
                if request.FILES.get('picture_post') is not None:
                    post = BlockPost.objects.create(user_post=user_,title=request.POST['title'],post=request.POST['post'],picture_post=request.FILES['picture_post'])
                    post.save()
                else:
                    post = BlockPost.objects.create(user_post=user_,title=request.POST['title'],post=request.POST['post'])
                    post.save()
                messages.success(request,'Post Content Successfully')
                del user_,formpost,post
                return redirect('profile')
            else:
                del user_,formpost
                return redirect('profile')
        else:
            return redirect('profile')
    else:
        user = User.objects.get(username=request.user)
        form = FormUser(instance=user)
        user_id = User.objects.get(username=user)
        img = DataUser.objects.get(user=user_id).picture.url
        data = DataUser.objects.get(user=user_id)
        form2 = Formdatauser(instance=data)
        form3 = FormPost()
        post_manage = BlockPost.objects.filter(user_post=user)
        post_value = BlockPost.objects.filter(user_post=user).values()
        count_comment =  CommentPost.objects.all().values('position_post_id')
        contaxt = {'form':form,'img':img,'form2':form2,'form3':form3,'manage':post_manage,'value':post_value,'cmt':count_comment}
        del user_id,data,form,img,form2,form3,post_manage,post_value,user,count_comment
        return render(request,'profile_page.html',contaxt)
    
@login_required(login_url='login')
def blockPage(request):  ## Block Public
    if request.method == 'POST':
        if request.POST.get('back') is not None:
            return redirect('profile')
        if request.POST.get('logout') is not None:
            logout(request=request)
            return redirect('login')
        else:
            return redirect('block')
    else:
        post = BlockPost.objects.all().values()
        name_user = User.objects.all().values('id','username')
        img = DataUser.objects.all().values('user_id','picture')
        user = User.objects.get(username=request.user).username
        count_comment =  CommentPost.objects.all().values('position_post_id')
        contaxt = {'post':post,'user':user,'name':name_user,'img':img,'cmtb':count_comment}
        del post,user,name_user,img,count_comment
        return render(request,'block_page.html',contaxt)

@login_required(login_url='login') ## Manage Post
def manage(request,pk):
    if request.method == 'POST':
        if request.POST.get('btn-edit') is not None:
            edit = FormPost(request.POST)
            if edit.is_valid():
                new_edit = BlockPost.objects.get(id=pk)
                new_edit.title = request.POST['title']
                new_edit.post = request.POST['post']
                if request.FILES.get('picture_post') is not None:
                    new_edit.picture_post.delete()
                    new_edit.picture_post = request.FILES.get('picture_post')
                else:
                    new_edit.picture_post = BlockPost.objects.get(id=1).picture_post
                new_edit.save()
                del new_edit,edit,pk
                messages.success(request,'Update Post Complete')
                return redirect('profile')
            else:
                return redirect(reverse('manage',kwargs={'pk':pk})) 
        if request.POST.get('btn-delete') is not None:
            delete_post = BlockPost.objects.get(id=pk)
            delete_post.delete()
            del delete_post,pk
            return redirect('profile')
        if request.POST.get('btn-back') is not None:
            del pk
            return redirect('profile')
        else:
            return redirect(reverse('manage',kwargs={'pk':pk}))
    else:
        post = BlockPost.objects.get(id=pk)
        form = FormPost(instance=post)
        contaxt = {'form':form,'pk':pk}
        del post,form
        return render(request,'manage_post.html',contaxt)
    
@login_required(login_url='login') ## Join Post  
def joinPost(request,pk):
    if request.method == 'POST':
        if request.POST.get('btn-back_j') is not None:
            return redirect('block')
        if request.POST.get('btn-comment_j') is not None:
            if request.POST['comment'] == '':
                messages.error(request,'not comment information')
                return redirect(reverse('join',kwargs={'pk':pk}))
            else:
                user = User.objects.get(id=request.user.id)
                post_position = BlockPost.objects.get(id=pk)
                if request.FILES.get('btn-pic_j') is not None:
                    comment_post = CommentPost.objects.create(comment=request.POST['comment'],position_post=post_position,user_comment=user,picture_comment=request.FILES['btn-pic_j'])
                else:
                    comment_post = CommentPost.objects.create(comment=request.POST['comment'],position_post=post_position,user_comment=user)
                comment_post.save()
                del user,post_position,comment_post
                messages.success(request,'comment post successfully')
                return redirect(reverse('join',kwargs={'pk':pk}))
        else:
            return redirect(reverse('join',kwargs={'pk':pk}))
    else:
        post_id = BlockPost.objects.get(id=pk)
        img_profile = DataUser.objects.get(user_id=post_id.user_post_id).picture.url
        data_comment = CommentPost.objects.filter(position_post_id=pk).values()
        usercomment = DataUser.objects.all().values('user_id','picture')
        nameuser = User.objects.all().values('id','username')
        contaxt = {'pk':pk,'post':post_id,'img':img_profile,'user':post_id.user_post,'value_comment':data_comment,'user_c':usercomment,'name':nameuser,'check_user':request.user}
        del post_id,img_profile,data_comment,usercomment,nameuser
        return render(request,'join_post.html',contaxt)

@login_required(login_url='login') ## manage comment
def editComment(request,pk):
    if request.method == 'POST':
        if request.POST.get('btn-edit_cmt') is not None:
            edit_comment = CommentPost.objects.get(id=pk)
            if request.FILES.get('btn_pic_cmt') is not None:
                edit_comment.picture_comment.delete()
                edit_comment.picture_comment = request.FILES['btn_pic_cmt']
            else:
                pass
            edit_comment.comment = request.POST['edit_comment']
            edit_comment.save()
            del edit_comment
            return redirect(reverse('join',kwargs={'pk':CommentPost.objects.get(id=pk).position_post_id}))
        if request.POST.get('btn-delete_cmt') is not None:
            delete_comment = CommentPost.objects.get(id=pk)
            if str(delete_comment.picture_comment) != '':
                delete_comment.picture_comment.delete()
            else:
                pass
            position_post_delete_comment = int(CommentPost.objects.get(id=pk).position_post_id)
            delete_comment.delete()
            del delete_comment,pk
            return redirect(reverse('join',kwargs={'pk':position_post_delete_comment}))
        if request.POST.get('btn-back_cmt') is not None:
            return redirect(reverse('join',kwargs={'pk':CommentPost.objects.get(id=pk).position_post_id}))
        else:
            return redirect('profile')
    else:
        edit_cmt = CommentPost.objects.get(id=pk)
        contaxt = {'data_comment':edit_cmt}
        del edit_cmt
        return render(request,'manage_cmt.html',contaxt)

@login_required(login_url='login') ## Good Post    
def goodPost(request,gp):
    post_good = BlockPost.objects.get(id=gp)
    good = post_good.good_post
    post_good.good_post = good+1
    post_good.save()
    del post_good,good
    return redirect(reverse('join',kwargs={'pk':gp}))

@login_required(login_url='login') ## Good Comment  
def goodComment(request,gc,id):
    comment_good = CommentPost.objects.get(id=gc)
    good= comment_good.good_comment
    comment_good.good_comment = good+1
    comment_good.save()
    del comment_good,good,gc
    return redirect(reverse('join',kwargs={'pk':id}))