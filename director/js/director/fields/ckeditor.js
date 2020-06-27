/*
>->front/ckedit.rst>
==========
ckeditor
==========
源文件:vuejs/ckeditor.js

使用时，引入fields.pack.js即可。

使用示例
=========
::

	bus=new Vue()  //因为ckeditor的数据不是时时同步的，所以提交时，需要触发数据同步
	// 提交时:
	bus.$emit('sync_data')

	<ckeditor set='complex' config='{}'></ckeditor>

set
======

set是指预先定义好的一套设置。可以在Vue component中定义映射。

当前有的set有:

=========   ========
complex     完善
edit        普通编辑
=========   =========

<<<<
 */

var ck_complex = {
	// Define changes to default configuration here.
	// For complete reference see:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// The toolbar groups arrangement, optimized for two toolbar rows.
	toolbarGroups : [
		{ name: 'tools' },
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'forms' },
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'others' },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'styles' },
		{name:'font'},
		{ name: 'colors' },
		{ name: 'about' },
	],



	// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	removeButtons : 'Underline,Subscript,Superscript',

	// Set the most common block elements.
	format_tags : 'p;h1;h2;h3;pre',

	// Simplify the dialog windows.
	removeDialogTabs : 'image:advanced;link:advanced',
	image_previewText:'image preview',
	imageUploadUrl: '/d/ckeditor_image',// '/_face/ckeditor_upload_image',
	filebrowserImageUploadUrl: '/d/ckeditor_image',// '/_face/ckeditor_upload_image', // Will be replace by imageUploadUrl when upload_image
	extraPlugins : 'justify,codesnippet,lineutils,mathjax,colorbutton,uploadimage,font,autogrow,html5video,widget,widgetselection,clipboard,lineutils', //autogrow,
	mathJaxLib : 'https://cdn.mathjax.org/mathjax/2.6-latest/MathJax.js?config=TeX-AMS_HTML',
	extraAllowedContent :'img[class]',
	autoGrow_maxHeight : 600,
	autoGrow_minHeight:200,
	autoGrow_onStartup:true,
	autoGrow_bottomSpace:50,
	baseFloatZIndex : 99891014, //  > layer
	//height:800,
};


var ckeditor = {
	template:`<div class='ckeditor'>
		    	<textarea class="form-control" :maxlength="maxlength"></textarea>
	    	</div>`,
	props:{
		value:{},
		config:{},
		set:{
			default:'edit',
		},
		maxlength:{},
	},
	created:function(){
		debugger;
		//var self=this
		//eventBus.$on('sync_data',function(){
		//	self.$emit('input',self.editor.getData())
		//})
	},
	watch:{
		value:function(v){
			var self=this
			if(! self.ckeditor_loaded){
				self.ckeditor_setvalue_queue=function(){
					self.editor.setData(v, {
						callback: function() {
							this.resetDirty(); // true
						}
					})

					//self.editor.setData(v)
					//self.editor.resetDirty()
				}
			}else{
				self.editor.setData(v, {
					callback: function() {
						this.resetDirty(); // true
					}
				})

			}

		}
	},
	mounted:function () {
		var self=this
		self.input=$(this.$el).find('textarea')[0]
		var config_obj={
			//'complex':'//res.enjoyst.com/js/ck/config_complex.js',
			'complex':ck_complex,
			'edit':edit_level,
		}
		var config={}
		ex.assign(config,config_obj[self.set]) 
		ex.assign(config,self.config)
		// 4.5.10   4.6.2   ///static/lib/ckeditor4.6.2.js
		//
		//ex.load_js('https://cdn.bootcss.com/ckeditor/4.6.2/ckeditor.js',function(){
			//CKEDITOR.timestamp='GABCDFDGff'
			//self.input.value=self.value

		//CKEDITOR.plugins.addExternal('html5video', 'https://cdn.jsdelivr.net/gh/coblan/static@0.0/ckeditor/plugins/html5video/dialogs', 'html5video.js');

			var editor = CKEDITOR.replace(self.input,config)
			if(self.value){
				editor.setData(self.value)
				editor.resetDirty()
			}
			self.editor = editor

			editor.on('instanceReady',function(evt){
				self.ckeditor_loaded=true
				if(self.ckeditor_setvalue_queue){
					self.ckeditor_setvalue_queue()
				}
			})

			//var is_changed=false
			//editor.on( 'change', function( evt ) {
			//	// getData() returns CKEditor's HTML content.
			//	is_changed=true
			//	//self.$emit('input',editor.getData())
			//});
            //
			//setInterval(function(){
			//	if(is_changed){
			//		self.$emit('input',editor.getData())
			//		is_changed=false
			//	}
			//},3000)
		//})

	},
	//events:{
	//	'sync_data':function () {
	//		this.model=this.editor.getData()
	//	}
	//}
}
	//<script src="//cdn.ckeditor.com/4.10.1/full/ckeditor.js"></script>
Vue.component('ckeditor',function(resolve,reject){
	//ex.load_js('https://cdn.bootcss.com/ckeditor/4.6.2/ckeditor.js',function(){
	//ex.load_js('http://cdn.ckeditor.com/4.10.1/full/ckeditor.js',function(){
	//ex.load_js('/static/ckeditor_4.10.1/ckeditor/ckeditor.js',function(){
	ex.load_js(cfg.js_lib.ckeditor,function(){
		resolve(ckeditor)


		//CKEDITOR.plugins.setLang( 'html5video', 'zh-cn', {
		//	button: '插入HTML5视频',
		//	title: 'HTML5 视频',
		//	infoLabel: '视频信息',
		//	allowed: '允许上传格式: MP4, WebM, Ogv',
		//	urlMissing: '视频源地址丢失',
		//	videoProperties: '视频属性',
		//	upload: '上传',
		//	btnUpload: '上传到服务器',
		//	advanced: '高级',
		//	autoplay: '自动播放?',
		//	yes: '是',
		//	no: '否',
		//	responsive: '响应式宽度'
		//} );

	})
})


var edit_level = {
	// Define changes to default configuration here.
	// For complete reference see:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// The toolbar groups arrangement, optimized for two toolbar rows.
	toolbarGroups : [

		//{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'tools' },
		//{ name: 'clipboard',   groups: [  'undo' ] },
		//'/',
		{ name: 'basicstyles', groups: [  'undo','basicstyles', 'cleanup', ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align',  ] }, //'bidi',
		{ name: 'styles' },
		{name:'font'},
		{ name: 'colors' },

		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'forms' },
		{ name: 'others' },
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		//{ name: 'about' },
	],

// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	removeButtons : 'Underline,Subscript,Superscript',

	// Set the most common block elements.
	format_tags : 'p;h1;h2;h3;pre',

	// Simplify the dialog windows.
	//plugins : 'wysiwygarea,toolbar,basicstyles,...',
	removeDialogTabs : 'image:advanced;link:advanced',
	image_previewText:'image preview',
	imageUploadUrl:'/d/ckeditor_image', // '/_face/ckeditor_upload_image',
	filebrowserImageUploadUrl:'/d/ckeditor_image',// '/_face/ckeditor_upload_image', // Will be replace by imageUploadUrl when upload_image
	extraPlugins:'html5video,lineheight',
	allowedContent: true,
	//extraPlugins : 'justify,lineutils,colorbutton,uploadimage,font,autogrow', //,mathjax,codesnippet
	//removePlugins: 'html5video,forms,flash,a11yhelp,scayt,wsc,language,preview,print,save,saveall,template,newpage,templates',
	removePlugins: 'iframe,forms,flash,a11yhelp,scayt,wsc,language,preview,print,save,saveall,template,newpage,templates',
	mathJaxLib : '//cdn.mathjax.org/mathjax/2.6-latest/MathJax.js?config=TeX-AMS_HTML',
	extraAllowedContent :'img[class]',
	autoGrow_maxHeight : 600,
	autoGrow_minHeight:200,
	autoGrow_onStartup:true,
	autoGrow_bottomSpace:50,
	baseFloatZIndex : 99891014, //  > layer
//height:800,
};


