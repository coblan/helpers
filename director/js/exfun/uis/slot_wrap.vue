
<script>
    import slot_html from './slot_html.vue'

    export default{
        props:['ctx'],
        components:{
            slot_html
        },
        mounted(){
            if(this.ctx.css){
                ex.append_css(this.ctx.css)
            }
        },
        render(createElement){
            var slots=[]

            for(var i=0;i< this.ctx.slot.length;i++){
                var dc = this.ctx.slot[i]
                if(dc.editor){
                    slots.push(
                            createElement('template',{
                                slot:dc.name,
                            },[
                                createElement(dc.editor,{props:{ctx:dc} } )
                            ])
                    )
                }else if(dc.editors){
                    slots.push(
                            createElement('template',{
                                slot:dc.name,
                            },ex.map(dc.editors,item=>{
                                        if(item.editor){
                                            return createElement(item.editor,{props:{ctx:item} }  )
                                        }else{
                                            return  createElement(slot_html,{props:{html:item.html}} )
                                        }
                              } )
                            )
                    )

                }else{
                    slots.push(
                            createElement('template',{
                                slot:dc.name,
                            },[
                                createElement(slot_html,{props:{html:dc.html}} )
                            ])
                    )
                }

            }

            return createElement(
                    this.ctx.inn_editor,
                    {props:{ctx:this.ctx},
                        class:'com-slot-wrap'},
                    slots
            )
//            return createElement(
//                    'div',
//                    {},
//                    [
//                            createElement( 'com-title-html',
//                                    {props:{ctx:{html:'bbaa a '}}},
//                                    [
//                                            createElement('template',{
//                                                slot:'title'
//                                            },[
//                                                    createElement('h1','this is title')
//                                            ])
//                                    ]
//                            ),
//                            createElement( 'h1','wori')
//                    ]
//            )
        }

    }
</script>
