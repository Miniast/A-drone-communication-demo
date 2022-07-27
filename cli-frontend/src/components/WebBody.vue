<script setup lang="ts">
import { h, ref, Ref, watchEffect, onMounted, onBeforeUnmount } from 'vue'
import { useMessage } from 'naive-ui'
import { NAlert, NButton, NIcon, NSelect, NCollapse, NCollapseItem, NScrollbar } from 'naive-ui'
import type { MessageRenderMessage } from 'naive-ui'
import axios from 'axios'
import {
    DroneFront as DroneFrontIcon,
    Drone as DroneIcon
} from '@vicons/carbon'
import {
    ComputerFilled as ComputerIcon,
    ArrowForwardIosOutlined as ArrowIcon,
} from '@vicons/material'
window.$message = useMessage()

const linkState = ref<string>("未连接")
const datasetValue = ref(null)
const droneId = ref(null)
const droneInfo = ref({})
const records = ref([])
const menuOptions = ref([])
let droneUpdateTimer: any

function pad(num: number, cover: number) {
    return String("0".repeat(cover) + num).slice(-cover);
}
function getTime() {
    let dt = new Date();
    let y = dt.getFullYear();
    let mt = dt.getMonth() + 1;
    let day = dt.getDate();
    let h = dt.getHours();
    let m = dt.getMinutes();
    let s = dt.getSeconds();
    return y + '.' + mt + '.' + day + ' -  ' + pad(h, 2) + ' : ' + pad(m, 2) + ' : ' + pad(s, 2);
}


function register() {
    const url = 'http://127.0.0.1:5000/register'
    axios.get(url).then((res) => {
        console.log(res.data)
        droneId.value = res.data
    }).catch((error) => {
        console.log(error)
    })
}


function droneUpdate() {
    const url = 'http://127.0.0.1:5000/drone_info'
    axios.post(url, {
        droneId
    }).then((res) => {
        droneInfo.value = res.data
    }).catch((error) => {
        console.log(error)
    })
    droneUpdateTimer = setTimeout(droneUpdate, 10000)
}

const renderMessage: MessageRenderMessage = (props) => {
    const { content, type } = props
    console.log(props);
    return h(
        NAlert,
        {
            type: type === 'loading' ? 'default' : type,
            title: content,
            style: {
                boxShadow: 'var(--n-box-shadow)',
                maxWidth: 'calc(100vw - 32px)',
                width: '480px'
            }
        }
    )
}

function sendMessage(index: number) {
    if (datasetValue.value == null)
        window.$message.error("请选择数据", { render: renderMessage });
    else {
        const url = "./api/send_message"
        const message = {
            from: droneId,
            to: 'Server',
            time: getTime(),
            dataset: datasetValue.value
        }
        axios.post(url,).then(res => {
            console.log("success");
            records.value.push(message)
        })
    }
}

onMounted(async () => {
    let newOptions = []
    for (let i = 1; i <= 25; ++i) {
        newOptions.push({
            label: 'markSet' + String(i),
            value: i
        })
    }
    menuOptions.value = newOptions

    const res = await register()
    droneUpdate()
})
onBeforeUnmount(() => {
    clearTimeout(droneUpdateTimer)
})

</script>

<template>
    <div id='mainbox'>
        <div id='controlboard'>
            <div id="div1">
                <n-collapse :default-expanded-names="['1']">
                    <template #arrow>
                        <n-icon>
                            <computer-icon />
                        </n-icon>
                    </template>
                    <template #header-extra>
                        <n-icon>
                            <arrow-icon />
                        </n-icon>
                    </template>
                    <n-collapse-item title="传输控制" name="1">
                        <div class="statediv">
                            连接状态：{{ linkState }}
                        </div>
                        <div style="display:flex">
                            <div style="margin: 10px 0 5px 0; flex:2">数据传输：</div>
                            <n-select v-model:value="datasetValue" filterable placeholder="选择数据包" :options="menuOptions"
                                style="margin:5px 0 5px 0; flex:6" />
                            <n-button type='primary' style='margin:5px 10px 5px 10px; flex:1' @click="sendMessage">确认
                            </n-button>
                        </div>
                    </n-collapse-item>
                </n-collapse>
            </div>

            <!-- <div id="div2">
                <n-collapse>
                    <template #arrow>
                        <n-icon>
                            <drone-icon />
                        </n-icon>
                    </template>
                    <template #header-extra>
                        <n-icon>
                            <arrow-icon />
                        </n-icon>
                    </template>
                    <n-collapse-item title="传输控制" name="1">
                        <n-collapse accordion>
                            <template #arrow>
                                <n-icon>
                                    <drone-front-icon />
                                </n-icon>
                            </template>
                            <n-collapse-item v-for="(item, index) in droneList" :title="item.userName" name='1'
                                :style="'display:' + (item.state ? '' : 'none')">

                            </n-collapse-item>
                        </n-collapse>
                    </n-collapse-item>
                </n-collapse>
            </div>-->
        </div>
        <div id='printboard'>
            <div style="margin: 10px 0 0 20px; text-align:left">
                <h3>
                    通信记录：
                </h3>
            </div>
            <div class="myscrollbarbox">
                <n-scrollbar>
                    <span v-for="(item, index) in records">{{ item.time }} : transmission
                        markSet{{ item.dataset }} from {{ item.from }} to {{ item.to }} <br /></span>
                </n-scrollbar>
            </div>
        </div>
    </div>
</template>

<style>
#mainbox {
    display: flex;
    flex-flow: row nowrap;
    margin: 0 auto;
    width: 90%;
    height: 600px;
}

#printboard {
    flex: 3;
    margin: 20px 60px 20px 100px;
    background-color: white;
    padding: 20px 20px 20px 20px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
}

#controlboard {
    flex: 2;
    margin: 20px 20px 20px 20px;
    padding: 20px 20px 20px 20px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    text-align: left;
}

#div1 {
    margin: 20px 20px 20px 20px;
}

#div2 {
    margin: 20px 20px 20px 20px;
}

.myscrollbarbox {
    margin: 10px 10px 20px 20px;
    padding: 10px 10px 20px 20px;
    background-color: rgba(198, 198, 198, 0.6);
    text-align: left;
    width: 90%;
    height: 80%;
    border-radius: 10px;
}

.mybtn {
    width: 100%;
    height: 100%;
}

.statediv {
    margin: 10px 0 10px 0;
}
</style>