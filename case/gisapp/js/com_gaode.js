
require('./scss/com_gaode.scss')

var com_gaode={
    // 高德地图封装

    template:`<div id="container"></div>`,
    mounted:function(){
        this.onInit()
    },
    methods:{
        onInit:function(){
            this.editorTool,this.map = new AMap.Map(this.$el, {
                resizeEnable: true,
                center: [116.403322, 39.900255],//地图中心点
                zoom: 13 //地图显示的缩放级别
            });
        },
        addMark:function(marker){
            marker.setMap(map_com.map)
        }
    }
}

Vue.component('com-gaode',function(resolve,reject){
    ex.load_css(cfg.js_lib.gaode_css)

    ex.load_js(cfg.js_lib.gaode_js,function(){
        ex.load_js(cfg.js_lib.gaode_addtoolbar_js,function(){
            resolve(com_gaode)
        })
    })
})


/*

红圈
var redCircle= new AMap.Marker({
    icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
    position: [lon,lat],
    //title:ex.template('{bigclass}/{litclass}',row),
    content:'<div class="red circle"></div>'
})

蓝圈
var blueCircle= new AMap.Marker({
    icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
    position: lcase.loc,
    //title: ex.template('{bigclass}/{litclass}/{subtime}',lcase),
    content:'<div class="blue circle"></div>'
})

设置点击事件
AMap.event.addListener(marker, 'click', function() {
    var url = ex.template('http://10.231.18.25/CityGrid/CaseOperate_flat/ParticularDisplayInfo.aspx?taskid={taskid}',lcase)
    window.open(url)
    this.setContent('<div class="dark circle"></div>')
});


 map_com.map.setFitView()

 */

