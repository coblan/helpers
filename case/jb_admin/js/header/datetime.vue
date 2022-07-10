<template>
  <li class="datetime-pannel">
    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
        <i class="fa fa-calendar" aria-hidden="true"></i>
        <span>星期{{week}}</span>
        <span style="display: inline-block;margin: 0 3px;">{{date}}</span>
        <i class="fa fa-clock-o" aria-hidden="true"></i>
        <span>{{time}}:{{pad(second)}}</span>
    </a>
  </li>
</template>
<script>
export default {
  data(){
    return {
      date:'',
      week:'',
      time:'',
      second:0,
    }
  },
  mounted(){
    this.update()
    setInterval(()=>{
      this.updateSecond()
    },1000)

  },

  methods:{
    pad(number){
      return `${number}`.padStart(2,0)
    },
      update(){
        var now = ex.dayjs()
        this.date = now.format('YYYY/MM/DD')
        this.week = now.format('d')
        if(now.hour() >12){
          this.time = '下午'+ now.format('HH:mm')
        }else{
          this.time = '上午'+ now.format('HH:mm')
        }
        this.second = now.second()
      },
      updateSecond(){
        if(this.second ==59){
          this.update()
        }else{
          this.second +=1
        }
      }
  },

}
</script>
<style scoped lang="scss">
.datetime-pannel{
  float: left;
  white-space: nowrap;
}
</style>