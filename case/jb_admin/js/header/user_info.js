
var user_info={
    props:['head'],
    template:` <li class="dropdown user user-menu">
                        <!-- Menu Toggle Button -->
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <!-- The user image in the navbar-->
                            <!--<img src="dist/img/user2-160x160.jpg" class="user-image" alt="User Image">-->
                            <i class="fa fa-user-circle-o"></i>

                            <!-- hidden-xs hides the username on small devices so only the image appears. -->
                            <span class="hidden-xs" v-text="head.first_name || head.username">
                            </span>
                        </a>
                        <ul class="dropdown-menu">
                            <!-- The user image in the menu -->
                            <li class="user-header" style="font-size: 3em;">
                                <!--<img src="dist/img/user2-160x160.jpg" class="img-circle" alt="User Image">-->
                                <i class="fa fa-user-circle-o fa-lg"></i>
                                <p v-text="head.first_name || head.username">
                                </p>
                            </li>
                            <!-- Menu Body -->
                            <!--<li class="user-body">-->
                                <!--<div class="row">-->
                                    <!--<div class="col-xs-4 text-center">-->
                                        <!--<a href="#">Followers</a>-->
                                    <!--</div>-->
                                    <!--<div class="col-xs-4 text-center">-->
                                        <!--<a href="#">Sales</a>-->
                                    <!--</div>-->
                                    <!--<div class="col-xs-4 text-center">-->
                                        <!--<a href="#">Friends</a>-->
                                    <!--</div>-->
                                <!--</div>-->
                                <!--&lt;!&ndash; /.row &ndash;&gt;-->
                            <!--</li>-->
                            <!-- Menu Footer-->
                            <li class="user-footer">
                                <div class="pull-left">
                                    <a href="/accounts/pswd" class="btn btn-default btn-flat" v-text="tr.change_password"></a>
                                </div>
                                <div class="pull-right">
                                    <a href="/accounts/logout" class="btn btn-default btn-flat" v-text="tr.logout"></a>
                                </div>
                            </li>
                        </ul>
                    </li>`,
    data:function(){
        return {
            tr:cfg.tr
        }
    }
}



Vue.component('com-headbar-user-info',user_info)