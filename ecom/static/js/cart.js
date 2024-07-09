var updateBtns = document.getElementsByClassName('update-cart')

for(i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var ProductId = this.dataset.product
        var action =  this.dataset.action
        console.log('ProductId:', ProductId, 'action:', action)
        console.log('USER:', user)
        if(user==='AnonymousUser'){
            addCookieItem(ProductId, action)
                
        }
        else{
            updateUserOrder(ProductId, action)
        }
    })
    }

    function addCookieItem(productId, action){
        console.log("User not logged in!!!!!!")
        if (action == 'add'){
        if (cart[productId] == undefined){
        cart[productId] = {'quantity':1}

        }else{
            cart[productId]['quantity'] += 1
        }
    }

        if (action == 'remove'){
            cart[productId]['quantity'] -= 1

            if (cart[productId]['quantity'] <= 0){
                    console.log('Item should be deleted')
                    delete cart[productId];
        }
    }
    console.log('CART:', cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
    
    


    }

    

    function updateUserOrder(ProductId,action){     
        console.log('User is logged in, sending data...')
        var url = '/updateItem/'

        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type':'apllication/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'ProductId': ProductId, 'action':  action})
        })

        .then((response) =>{
            return response.json()
        })

        .then((data) =>{
            console.log('data:', data)
            location.reload()
        })




}