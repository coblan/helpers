import {com_sim_fields} from  './sim_fields'

export var  suit_fields= {
    props:['row','heads','ops'],
    mixins:[com_sim_fields],


    template:`<div class="flex-v" style="margin: 0;height: 100%;">
    <div class = "flex-grow" style="overflow: auto;margin: 0;">
        <div class="field-panel suit" >
            <field  v-for="head in normed_heads" :key="head.name" :head="head" :row="row"></field>
        </div>
      <div style="height: 1em;">
      </div>
    </div>
    <slot>
         <div style="text-align: right;padding: 8px 3em;">
         <button @click="submit" type="btn"
                            :class="['btn',btnCls]"><span v-text="okBtn">保存</span></button>
        <!--<component v-for="op in ops" :is="op.editor" @operation="on_operation(op)" :head="op"></component>-->
        </div>
    </slot>

     </div>`,

}

