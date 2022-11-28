(function (window, undefined) {
'use strict';
let fileUpload = document.getElementById('file-uploader');
let previewImg = document.getElementById('preview');
let button = document.getElementById('send-data')
fileUpload.addEventListener('change', (e) => {
    if (e.target.files[0]) previewImg.classList.remove('d-none');
    previewImg.src = URL.createObjectURL(e.target.files[0]);
});
})(window);


    $(document).ready(function(){
    
        let multipleCancelButton = new Choices('#choices-multiple-remove-button', {
        removeItemButton: true,
        maxItemCount:5,
        searchResultLimit:5,
        renderChoiceLimit:5
        }); 
    });

    const toggleRow = (element) => {
    element.getElementsByClassName('expanded-row-content')[0].classList.toggle('hide-row');
    }



(function(){

"use strict"


  // Plugin Constructor
let TagsInput = function(opts){
    this.options = Object.assign(TagsInput.defaults , opts);
    this.init();
}

  // Initialize the plugin
TagsInput.prototype.init = function(opts){
    this.options = opts ? Object.assign(this.options, opts) : this.options;

    if(this.initialized)
        this.destroy();
    if(!(this.orignal_input = document.getElementById(this.options.selector)) ){
        console.error("tags-input couldn't find an element with the specified ID");
        return this;
    }

    this.arr = [];
    this.wrapper = document.createElement('div');
    this.input = document.createElement('input');
    init(this);
    initEvents(this);
    this.initialized =  true;
    return this;
}

  // Add Tags
TagsInput.prototype.addTag = function(string){

    if(this.anyErrors(string))
        return ;

    this.arr.push(string);
    let tagInput = this;

    let tag = document.createElement('span');
    tag.className = this.options.tagClass;
    tag.innerText = string;

    let closeIcon = document.createElement('a');
    closeIcon.innerHTML = '&times;';
    
      // delete the tag when icon is clicked
    closeIcon.addEventListener('click' , function(e){
        e.preventDefault();
        let tag = this.parentNode;

        for(let i =0 ;i < tagInput.wrapper.childNodes.length ; i++){
            if(tagInput.wrapper.childNodes[i] == tag)
                tagInput.deleteTag(tag , i);
        }
    })


    tag.appendChild(closeIcon);
    this.wrapper.insertBefore(tag , this.input);
    this.orignal_input.value = this.arr.join(',');

    return this;
}

  // Delete Tags
TagsInput.prototype.deleteTag = function(tag , i){
    tag.remove();
    this.arr.splice( i , 1);
    this.orignal_input.value =  this.arr.join(',');
    return this;
}

  // Make sure input string have no error with the plugin
TagsInput.prototype.anyErrors = function(string){
    if( this.options.max != null && this.arr.length >= this.options.max ){
        console.log('max tags limit reached');
        return true;
    }
    
    if(!this.options.duplicate && this.arr.indexOf(string) != -1 ){
        return true;
    }

    return false;
}

  // Add tags programmatically 
TagsInput.prototype.addData = function(array){
    let plugin = this;
    
    array.forEach(function(string){
        plugin.addTag(string);
    })
    return this;
}

  // Get the Input String
TagsInput.prototype.getInputString = function(){
    return this.arr.join(',');
}

  // destroy the plugin
TagsInput.prototype.destroy = function(){
    this.orignal_input.removeAttribute('hidden');

    delete this.orignal_input;
    let self = this;
    
    Object.keys(this).forEach(function(key){
        if(self[key] instanceof HTMLElement)
            self[key].remove();
        
        if(key != 'options')
            delete self[key];
    });

    this.initialized = false;
}

  // Private function to initialize the tag input plugin
function init(tags){
    tags.wrapper.append(tags.input);
    tags.wrapper.classList.add(tags.options.wrapperClass);
    tags.orignal_input.setAttribute('hidden' , 'true');
    tags.orignal_input.parentNode.insertBefore(tags.wrapper , tags.orignal_input);
}

  // initialize the Events
function initEvents(tags){
    tags.wrapper.addEventListener('click' ,function(){
        tags.input.focus();           
    });
    

    tags.input.addEventListener('keydown' , function(e){
        let str = tags.input.value.trim(); 

        if( !!(~[9 , 13 , 188].indexOf( e.keyCode ))  )
        {
            e.preventDefault();
            tags.input.value = "";
            if(str != "")
                tags.addTag(str);
        }

    });
}


  // Set All the Default Values
TagsInput.defaults = {
    selector : '',
    wrapperClass : 'tags-input-wrapper',
    tagClass : 'tag',
    max : null,
    duplicate: false
}

window.TagsInput = TagsInput;

})();

let tagInput1 = new TagsInput({
        selector: 'tag-input1',
        duplicate : false,
        max : 10
    });
    tagInput1.addData(['Black'])



// Start Edit 
let $selectColor = $('#choices-multiple-colors')
let $selectSize = $('#choices-multiple-sizes')
    
    $(function() {
        $selectColor.multipleSelect()
        $selectSize.multipleSelect()
    
    })

    function post_url(element){
        slug = element.id;
        document.getElementById("postProduct").action = "update-product/"+slug ;
        data = document.getElementById("row-"+slug);
        name      = $(data).data("name");
        brand     = $(data).data("brand");
        price     = $(data).data("price");
        old_price = $(data).data("oldprice");
        quant     = $(data).data("quantity");
        gender    = $(data).data("gender");
        cat       = $(data).data("category");
        colors    = $(data).data("colors");
        sizes     = $(data).data("sizes");
        image     = $(data).data("image");
        details   = $(data).data("details");

        document.getElementById("product_name").value = name ;
        document.getElementById("brand_name").value = brand ;
        document.getElementById("price").value = price ;
        document.getElementById("price_dis").value = old_price ;
        document.getElementById("count").value = quant ;
        document.getElementById("gender").value = gender ;
        document.getElementById("category").value = cat ;
        document.getElementById("description").value = details ;
        
        //choices-multiple-colors
        const $col = document.querySelector('#choices-multiple-colors');
        $col.value = -1;
        $selectColor.multipleSelect('setSelects', colors)

        const $siz = document.querySelector('#choices-multiple-sizes');
        $siz.value = -1;
        $selectSize.multipleSelect('setSelects', sizes)

        window.scrollTo(0,document.body.scrollHeight);

    };
    function clear_url(){
        document.getElementById("postProduct").action = '' ;
        document.getElementById("product_name").value = '' ;
        document.getElementById("brand_name").value = '' ;
        document.getElementById("price").value = '' ;
        document.getElementById("price_dis").value = '' ;
        document.getElementById("count").value = '' ;
        document.getElementById("gender").value = -1;
        document.getElementById("category").value = -1 ;
        document.getElementById("description").value = '' ;

        
        //choices-multiple-colors
        const $col = document.querySelector('#choices-multiple-colors');
        $col.value = -1;

        const $siz = document.querySelector('#choices-multiple-sizes');
        $siz.value = -1;

    };
// End Edit 