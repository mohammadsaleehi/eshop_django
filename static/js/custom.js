function sendArticleComment(articleId) {
    var comment = $('#commentText').val();
    var parentId = $('#parentId').val();
    $.get('/articles/add-article-comment', {
        article_comment: comment, article_id: articleId, parent_id: parentId
    }).then(res => {
        $('#comments_area').html(res);
        $('#commentText').val('');
        $("#parentId").val('');
        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: 'smooth'});
        } else {
            document.getElementById('comment_scrol').scrollIntoView({behavior: 'smooth'});
        }
    });
    // ajax ->  asynchronous javascript and xml
    // json ->  javascript object notation
}

function fillParentId(parentId) {
    $('#parentId').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: 'smooth'});
}

function fillterProducts() {
    const filterPrice = $('#sl2').val().split(',');
    const start_price = filterPrice[0];
    const end_price = filterPrice[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $("#filter_price").submit();
}


function fillPage(page) {
    $('#page').val(page);
    $("#filter_price").submit();
}


function showLargeImage(ImageSrc) {
    $('#main_image').attr('src', ImageSrc);
    $('#show_large_image_modal').attr('href', ImageSrc);
}

function sendProductComment(productId) {
    var comment = $('#commentText').val();
    $.get('/products/add-product-comment', {
        product_comment: comment, product_id: productId
    }).then(res => {
        $('#reviews').html(res);
        $('#commentText').val('');
        document.getElementById('comment_scrol').scrollIntoView({behavior: 'smooth'});
    });
    // ajax ->  asynchronous javascript and xml
    // json ->  javascript object notation
}

function addProductToOrder(productId) {
    const count = $('#count').val();
    $.get('/order/add-to-order/', {
        product_id: productId, count: count
    }).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            confirmButtonColor: '#3085d6',
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfrimed && res.status === 'not_auth') {
                window.location.href = '/login/';
            }
        });

        /*if (res.status === 'success') {
            Swal.fire({
                title: 'اعلان',
                text: "محصول مورد نظر شما با موفقیت به سبد خرید شما اضافه شد",
                icon: 'success',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'باشه ممنون'
            });
        }else if (res.status === 'not_found'){
             Swal.fire({
                title: 'اعلان',
                text: "محصول مورد نظر شما با موفقیت به سبد خرید شما اضافه شد",
                icon: 'error',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'باشه ممنون'
            });
        }*/

    });
    $("#count").val(1);
}

function removeOrderDetail(detailId) {
    $.get("/user/remove-order-detail?detail_id=" + detailId).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}

// detail id => order Detail Id
// state => increase, decrease
function changeOrderDetailCount(detailId, state) {
    $.get("/user/change-order-detail?detail_id=" + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}

function deleteAdminPanelArticle(articleId) {
    Swal.fire({
        title: 'مطمئنی میخوای مقاله رو حذف کنی؟',
        text: "چرا به جای غیر فعال کردن می خوای حذف کنی!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#9f9b9b',
        confirmButtonText: 'آره حذف کن',
        cancelButtonText: "نه نمی خوام"
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                'حذف شد',
                "شما این مقاله رو حذف کردید",
                'success'
            )
            $.get('/admin-panel/article/delete/' + articleId + "/").then(res => {
                window.location.reload();
            })
        }
    })
}

function fillOrderBy(value_name) {
    $('#ord_id').val(value_name);
}

function fillPageArticle(page) {
    $('#page').val(page);
    $('#order_article').submit();
}

function fillOrderArticle(order) {
    $('#order').val(order);
}

function orderArticle() {
    $("#order_article").submit();
}

