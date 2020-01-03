Vue.component('com-van-grid',{
    props:['ctx'],
    template:`<div>
    <!--<van-button type="default">默认按钮</van-button>-->
    <van-grid square>
        <van-grid-item
                v-for="head in ctx.heads"
                icon="photo-o"
                :text="head.label"
        />
    </van-grid>
    </div>`
})