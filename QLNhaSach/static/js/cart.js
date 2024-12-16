function update_receipt_detail(receiptId){
   fetch(`/${receiptId}`,{
     method: "update",
     headers: location.reload(),
     body: window.location = '/admin/hoadonview'
   })
}

function updateCart(productId, obj, quantity, soluongton) {
   var kiemtra = (soluongton + quantity) - obj.value;
   if (kiemtra < 0){ alert("Không thể thêm số lượng vì số lượng trong kho so với số lượng hiện tại là" + ((soluongton + quantity) - obj.value));
          obj.value = quantity
   }
   else{
   fetch(`/api/cart/${productId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementsByClassName('cart-amount')
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString("en-US")
    }).catch(err => console.info(err)) // promise
    }
}

function deleteCart(productId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/api/cart/${productId}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            let d = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let d2 = document.getElementsByClassName('cart-amount')
            for (let i = 0; i < d2.length; i++)
                d2[i].innerText = data.total_amount.toLocaleString("en-US")

            let c = document.getElementById(`cart${productId}`)
            c.style.display = "none"
        }).catch(err => console.info(err)) // promise
    }
}

function pay_online() {
    if (confirm("Bạn chắc chắn thanh toán không?") == true) {
        fetch("/api/pay_online").then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload()
            else
                alert("Hệ thống đang bị lỗi!")
        })
    }
}


function pay_offline() {
    if (confirm("Bạn có muốn đặt hàng") == true) {
        fetch("/api/pay_offline").then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload()
            else
                alert("Hệ thống đang bị lỗi!")
        })
    }
}