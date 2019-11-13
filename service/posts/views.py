from urllib.parse import quote
from django.shortcuts import( render,get_object_or_404,redirect)
from django.http import( HttpRequest,HttpResponse,HttpResponseRedirect,Http404,JsonResponse)
from django.contrib.contenttypes.models import ContentType
from  posts.models import Post,Post_user_fav
from comments.models import Comment
from django.utils import timezone
from next_prev import next_in_order, prev_in_order
from accounts.models import UserProfile
#from .forms import PostForm
from category.models import Category
from django.db.models import Count    
from comments.forms import CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned



def post_detail(request,id):
    if not request.user.is_authenticated  :
        print ("not=========")
        return HttpResponseRedirect("/login")
    elif Post.objects.filter(id=id).exists()==True:
        #obj=Post.objects.all().order_by("updated")
        obj=get_object_or_404(Post,id=id)
        nexto = next_in_order(obj, loop=True)
        prev = prev_in_order(obj, loop=True)
        share_string=quote(obj.content)

        initial_data={
            "content_type":obj.get_content_type,
            "object_id":obj.id
        }

        form=CommentForm(request.POST or None ,initial= initial_data)
        if form.is_valid():
            c_type=form.cleaned_data.get("content_type")
            content_type=ContentType.objects.get(model=c_type)
            obj_id=form.cleaned_data.get('object_id')
            content_data=form.cleaned_data.get('content')
            parent_obj=None
            try:
               parent_id=int(request.POST.get("parent_id"))
            except:
                parent_id=None

            if parent_id:
                parent_qs=Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj =parent_qs.first()              
            new_comment,created=Comment.objects.get_or_create(
               user=request.user,
               content_type=content_type,
               object_id=obj_id,
               content=content_data,
               timestamp=timezone.now(),
               parent=parent_obj
            )   
        import array as arr    
        global post_count,posts,user_fav
        comments=obj.comments
        usernow=request.user
        category_post = Category.objects.all().annotate(posts_count=Count('post'))
        p=Post.objects.all().order_by('-timestamp')[:5]
        post_fav = get_object_or_404(Post, pk=id)
        userf=UserProfile.objects.get(user=usernow)
        user_fav=UserProfile.objects.filter(favourites=post_fav)
        if user_fav:
            print(user_fav)
        
        #get_object_or_404(UserProfile,favourites=post_fav).first()
       
        try:
            if post_fav.is_favorite:
                userf.favourites.add(post_fav)
                post_fav.is_favorite = False
            else:
                post_fav.is_favorite = True
                #userf.delete(favourites)
            post_fav.save()
            
        except (KeyError, Post.DoesNotExist):
            return JsonResponse({'success': False})
        
        context={
            "obj":obj ,
            "share_string":share_string,
            "comments":comments,
            "comment_form":form,
            'usernow':usernow,
            "next":nexto,
            "prev":prev,
            "post_count":category_post,
            "posts":p,
            "user_fav":user_fav
    
        }
        return render(request,"blog-details.html",context)
    else:
         return HttpResponse("no obj")



def index(request):
    if not request.user.is_authenticated  :
        print ("not=========")
        return HttpResponseRedirect("/login")
    obj=Post.objects.all()
    paginator = Paginator(obj, 4) # Show 25 contacts per page
    page = int(request.GET.get('page', '1'))
    contacts = paginator.page(page)
    category_post = Category.objects.all().annotate(posts_count=Count('post'))
    p=Post.objects.all().order_by('-timestamp')[:5]
    context={
            "obj":contacts ,
            "post_count":category_post,
            "posts":p,
    }
    return render(request,"category.html",context)

def archived(request):
    if not request.user.is_authenticated  :
        print ("not=========")
        return HttpResponseRedirect("/login")
    obj=Post.objects.filter(is_archived=True)
    paginator = Paginator(obj, 4) # Show 25 contacts per page
    page = int(request.GET.get('page', '1'))
    contacts = paginator.page(page)
    category_post = Category.objects.all().annotate(posts_count=Count('post'))
    p=Post.objects.all().order_by('-timestamp')[:5]
    context={
            "obj":contacts ,
            "post_count":category_post,
            "posts":p,
    }
    return render(request,"archive.html",context)


def home(request):
    if not request.user.is_authenticated  :
        print ("not=========")
        return HttpResponseRedirect("/login")
    obj=Post.objects.all().order_by("publish")[:8]
    paginator = Paginator(obj, 4) # Show 25 contacts per page
    page = int(request.GET.get('page', '1'))
    contacts = paginator.page(page)
    category_post = Category.objects.all().annotate(posts_count=Count('post'))
    p=Post.objects.all().order_by('-timestamp')[:5]
    context={
            "obj":obj ,
            "post_count":category_post,
            "posts":p,
            "contacts":contacts
    }
    return render(request,"index.html",context)

# def favourite(request, pk):
#         favourite = Post.objects.get(pk=pk)
#         user = request.user
#         user.favourites.add(favourite)
#         return redirect("blog-details.html")

# def favorite_project(request, post_fav_id):
#     post_fav = get_object_or_404(Post, pk=post_fav_id)
#     try:
#         if post_fav.is_favorite:
#             post_fav.is_favorite = False
#         else:
#             post_fav.is_favorite = True
#         post_fav.save()
#     except (KeyError, post_fav.DoesNotExist):
#         return JsonResponse({'success': False})
#     else:
#         return JsonResponse({'success': True})

# def ajax_is_favorite(request):
#     return
#     # if not request.is_ajax() or not request.method=='POST':
#     #     return HttpResponseNotAllowed(['POST'])
#     # else:
#     #    projectprofile = get_object_or_404(Post, pk=projectprofile_id)
#     # try:
#     #     if projectprofile.is_favorite:
#     #         projectprofile.is_favorite = False
#     #     else:
#     #         projectprofile.is_favorite = True
#     #     projectprofile.save()
#     # except (KeyError, ProjectProfile.DoesNotExist):
#     #     return JsonResponse({'success': False})
#     # else:
#     #     return JsonResponse({'success': True})

def contacts(request):
   return render(request,"contact.html")

def unique(request,word):
   u=Post.objects.filter(uniquewords=word)[:1]
  
   return render(request,"blog-detail.html",context)