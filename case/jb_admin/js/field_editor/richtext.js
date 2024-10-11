Vue.component('com-field-richtext',{
    props:['row','head'],
    template:`<div class="com-field-richtext">
            <div v-if='head.readonly' v-html='row[head.name]'></div>
            <div v-else>
                <ckeditor v-if="loaded" ref="ck" :style="head.style" v-model="inn_data"
                :maxlength='head.maxlength'
                :id="'id_'+head.name" :set="head.set" :config="head.config"></ckeditor>
                <div style="height: 1em;width: 0;position: relative">
                <input type="text" :name='head.name' style="display: none"  v-model="row[head.name]">
                </div>
            </div>
<!--            <div>-->
<!--                <input type="file" @change="onChange">-->
<!--                hello  <img :src="test_img" alt="" style="width: 100px;height: 100px;">-->
<!--            </div>-->
           
         </div>`,
    async mounted(){
        if(this.head.mounted_express){
            ex.eval(this.head.mounted_express,{vc:this,})
        }
        if(this.head.css){
            ex.append_css(this.head.css)
        }

        if(this.head.aes=='ecb'){
            this.inn_data = await this.parseHtml(this.row[this.head.name])
        }else{
            this.inn_data = this.row[this.head.name]
        }

        this.loaded=true

        this.checkLive()

    },
    data(){
        return {
            loaded:false,
            inn_data:'',
            test_img:'',
            image_map:{}
        }
    },

    // unmounted(){
    //     alert('waw')
    // },
    // destroyed(){
    //     alert('dis')
    // },
    // deactivated () {
    //     alert('deacgive')
    // },
    methods:{
        // 本来应该调用 URL.revokeObjectURL(objectURL);
        // checkLive(){
        //     setTimeout(()=>{
        //         var self = this
        //         debugger
        //         // if(self.$el.checkVisibility()){
        //         //     alert('关闭了')
        //         // }else{
        //             this.checkLive()
        //         // }
        //
        //     },2000)
        // },
        onChange(event){
            var myfile = event.target.files[0]
            // var reader = new FileReader();
            // reader.readAsDataURL(myfile)
            var obj_url = URL.createObjectURL(myfile);
            this.test_img=obj_url
            // reader.onload = async (oFREvent)=>{
            //     debugger
            //     // this.test_img=reader.result;
            //     // await ex.load_js('https://lf6-cdn-tos.bytecdntp.com/cdn/expire-1-M/crypto-js/4.1.1/crypto-js.min.js')
            //     // var blob =  await DecryptBase(reader.result)
            //     debugger
            //     var obj_url = URL.createObjectURL(myfile);
            //     debugger
            //     this.test_img=obj_url
            // };



        },
        commit:function(){
            //
            var html =this.$refs.ck.editor.getData()
            if(this.head.aes=='ecb'){
                html = this.stringifyHtml(html)
            }
            Vue.set(this.row,this.head.name,html)
        },
        async parseHtml(html){
            var el = document.createElement( 'div' );
            el.innerHTML=html
            var self = this
            var imagelist= el.querySelectorAll('img')

            this.image_map ={}
            var ls =[]
            for(var i=0;i<imagelist.length;i++){
                var img=imagelist[i]
                var src = img.getAttribute('src')
                if(src.endsWith('aes')){
                    var pp = self.aesToBlob(src).then(blob=>{
                        if(blob){
                            var obj_url = URL.createObjectURL(blob);
                            img.setAttribute('src',obj_url)
                            self.test_img=obj_url
                            this.image_map[obj_url] = src
                        }

                    })
                    ls.push(pp)
                    // var blob = await self.aesToBlob(src)
                    // debugger
                    // var obj_url = URL.createObjectURL(blob);
                    // img.setAttribute('src',obj_url)
                }
            }
            await  Promise.all(ls)
            return el.innerHTML
        },
       async  aesToBlob(src){
            await ex.load_js('https://lf6-cdn-tos.bytecdntp.com/cdn/expire-1-M/crypto-js/4.1.1/crypto-js.min.js')
           try{
               var rt = await ex.getFile(src)
           }catch (e){
                console.log(e)
                return
           }
            var aes_info = await ex.keyCache('aes_info', async ()=>{
                return ex.director_get('upload/encrypt/info?entry=aes')
            })
            // var base = await Decrypt(rt,'94a4b778g01ca4ab')
            var blob = await Decrypt(rt,aes_info.key)
           return blob

        },
        stringifyHtml(html){
            var el = document.createElement( 'div' );
            el.innerHTML=html
            var self = this
            var imagelist= el.querySelectorAll('img')
            var ls =[]
            for(var i=0;i<imagelist.length;i++){
                var img=imagelist[i]
                var src = img.getAttribute('src')
                if(this.image_map[src]){
                    img.setAttribute('src',this.image_map[src]  )
                }
            }
            return el.innerHTML
        }
    }
})

async function Decrypt(data,key) {
    // var arrayBuffer =  await data.arrayBuffer()  // await  blobToArrayBuffer(data)
    // var wordArray = CryptoJS.lib.WordArray.create(arrayBuffer);
    var mydata = await blobToDataURL(data)
    var naked_base64= mydata.slice(37,)
    // var wordArray = CryptoJS.enc.Base64.parse()
    var AES_KEY = CryptoJS.enc.Utf8.parse(key); //key //
    var decrypted = CryptoJS.AES.decrypt(naked_base64, AES_KEY, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7 });
    // decrypted = decrypted.toString(CryptoJS.enc.Utf8)
    var bb = CryptoJS.enc.Base64.stringify(decrypted)
    return b64toBlob(bb)
    // debugger
    // return new Blob([decrypted], {type: "image/png"});
    // var buf = wordArrayToArrayBuffer(decrypted)
    // return new Blob(buf,{type: "image/png"});
    // var w = convertWordArrayToUint8Array(decrypt)
    // debugger
    // return Uint8ArrayToBlob(w)
    // var bb = CryptoJS.enc.Base64.stringify(decrypt)
    // var b2 = `data:application/octet-stream;base64,${bb}`
    // return b2
//    var u8 = convertWordArrayToUint8Array(decrypt)

    // return blob;
}
const b64toBlob = (b64Data, contentType='', sliceSize=512) => {
    const byteCharacters = atob(b64Data);
    const byteArrays = [];

    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        const slice = byteCharacters.slice(offset, offset + sliceSize);

        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
    }

    const blob = new Blob(byteArrays, {type: contentType});
    return blob;
}

// function blobToArrayBuffer(blob){
//     var pro = new ex.FreePromise()
//     var arrayBuffer;
//     var fileReader = new FileReader();
//     fileReader.onload = function(event) {
//         arrayBuffer = event.target.result;
//         // pro.resolve(arrayBuffer)
//         pro.resolve(fileReader.result)
//     };
//     fileReader.readAsArrayBuffer(blob);
//     return pro.promise
// }
function wordArrayToArrayBuffer(wordArray) {
    const { words } = wordArray
    const { sigBytes } = wordArray
    const u8 = new Uint8Array(sigBytes)
    for (let i = 0; i < sigBytes; i += 1) {
        u8[i] = (words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff
    }
    return u8
}

// function convertWordArrayToUint8Array(wordArray) {
//     var arrayOfWords = wordArray.hasOwnProperty("words") ? wordArray.words : [];
//     var length = wordArray.hasOwnProperty("sigBytes") ? wordArray.sigBytes : arrayOfWords.length * 4;
//     var uInt8Array = new Uint8Array(length), index=0, word, i;
//     for (i=0; i<length; i++) {
//         word = arrayOfWords[i];
//         uInt8Array[index++] = word >> 24;
//         uInt8Array[index++] = (word >> 16) & 0xff;
//         uInt8Array[index++] = (word >> 8) & 0xff;
//         uInt8Array[index++] = word & 0xff;
//     }
//     return uInt8Array;
// }
// function Uint8ArrayToBlob(data){
//     return new Blob(data,{type: "image/png"});
// }

function blobToDataURL(blob) {
    var pro = new ex.FreePromise()
    var a = new FileReader();
    a.onload = function(e) {
        pro.resolve(e.target.result)
        // callback(e.target.result);
    }
    a.readAsDataURL(blob);
    return pro.promise
    // return URL.createObjectURL(blob);
}