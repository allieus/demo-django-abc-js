from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import CommentForm
from blog.models import Post, Comment


def index(request):
    post_qs = Post.objects.all()

    return render(request, "blog/post_list.html", {
        "post_list": post_qs,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_qs = post.comment_set.all()
    comment_form = CommentForm()
    # comment_qs = Comment.objects.filter(post=post)
    return render(request, "blog/post_detail.html", {
        "post": post,
        "comment_list": comment_qs,
        "comment_form": comment_form,
    })


# ajax로만 요청됨을 가정
def comment_list(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_qs = post.comment_set.all()
    return render(request, "blog/_comment_list.html", {
        "comment_list": comment_qs,
        "post": post,
    })


@login_required
def comment_new(request, post_pk):
    # 현재 요청이 jQuery를 통한 요청인지 아닌지를 판단할 수 있어야 합니다.
    is_ajax = request.headers.get('X-Requested-With') == "XMLHttpRequest"

    post = get_object_or_404(Post, pk=post_pk)

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            if is_ajax:
                # comment에 대한 li html 응답을 줘야 합니다.
                form = CommentForm()
                return render(request, "blog/_comment_form.html", {
                    "form": form,
                    "comment_new_url": request.path,
                })
            else:
                # return redirect(f"/blog/{post_pk}/")
                return redirect("blog:post_detail", post_pk)
    else:
        form = CommentForm()

    if is_ajax:
        template_name = "blog/_comment_form.html"
    else:
        template_name = "blog/comment_form.html"

    is_errored = bool(form.errors)
    if is_errored:
        status_code = 400
    else:
        status_code = None

    return render(request, template_name, {
        "form": form,
        "comment_new_url": request.path,
    }, status=status_code)


@login_required
def comment_edit(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            # return redirect(f"/blog/{post_pk}/")
            return redirect("blog:post_detail", post_pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, "blog/comment_form.html", {
        "form": form,
    })


@login_required
def comment_delete(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_pk)

    return render(request, "blog/comment_confirm_delete.html", {
        "comment": comment,
    })
