<template>
    <div :class="['com-field-int','field-'+head.name,head.class]" >
        <span v-if='head.readonly && !head.prefix && !head.suffix' v-text='row[head.name]'></span>
        <div  v-else class="form-inline">


            <el-input v-model="row[head.name]" size="small" :placeholder="head.placeholder" :readonly="head.readonly"
                      :name="head.name"
                      :id="'id_'+head.name"
                      @keypress.native="isNumber($event)"
                      :autofocus="head.autofocus">
                <template slot="prepend" >
                    <span  v-if="head.prefix" v-html="head.prefix"></span>
                </template>
                <template slot="append">
                    <span  v-if="head.suffix" v-html="head.suffix"></span>
                </template>
            </el-input>

            <!--<div class="input-group" >-->
                <!--<div class="input-group-addon" v-if="head.prefix" v-html="head.prefix"></div>-->
                <!--<input  type="text" class="form-control input-sm" v-model="mydata" :id="'id_'+head.name"-->
                        <!--:style="{width:head.width}"-->
                        <!--:name="head.name" :step="head.step"-->
                        <!--@keypress="isNumber($event)"-->
                        <!--:readonly="head.readonly"-->
                        <!--:placeholder="head.placeholder" :autofocus="head.autofocus">-->
                <!--<div class="input-group-addon" v-if="head.suffix" v-html="head.suffix"></div>-->
            <!--</div>-->
        </div>

    </div>
</template>

<script>
    export default {
        props:['row','head'],
        data(){
          return {
              mydata:this.row[this.head.name]
          }
        },
        watch:{
          mydata(v){
              if(v || v==0){
                  this.row[this.head.name] = parseInt(v)
              }
          }
        },
        created(){
        },
        mounted(){

        },
        methods:{
            isNumber:function(evt){
                evt = (evt) ? evt : window.event;
                var charCode = (evt.which) ? evt.which : evt.keyCode;
                if(charCode== 46){
                    return evt.preventDefault();
                }

                if ((charCode >= 48 && charCode <= 57) || charCode== 46 || charCode== 45) {
                    if(charCode==46 && this.row[this.head.name].indexOf('.')!=-1){
                        return evt.preventDefault();
                    }else{
                        return true
                    }
                }else{
                    return evt.preventDefault();
                }
            }
        }
    }
</script>
