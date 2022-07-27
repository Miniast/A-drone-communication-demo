<template>
    <div class="console">
        <!--数据卡片-->
        <div class="drone-header">
            <n-grid cols="4" responsive="screen" :x-gap="20" :y-gap="8">
                <n-grid-item span="1">
                    <NCard title="无人机列表" :segmented="{ content: true, footer: true }" size="small" :bordered="false">
                        <template #header-extra>
                        </template>
                        <n-scrollbar style="height:220px">
                            <n-menu ref="menuInstRef" :options="droneOptions" @update:value="handleUpdateValue"
                                accordion />
                        </n-scrollbar>
                        <template #footer>
                            <div class="fill div">
                            </div>
                        </template>
                    </NCard>
                </n-grid-item>
                <n-grid-item span="2">
                    <NCard title="数据发送" :segmented="{ content: true, footer: true }" size="small" :bordered="false">
                        <n-scrollbar style="height:220px">
                            <div class="drone-header-data-sender-container">
                                <div class="drone-header-data-sender-container-label">数据传输：</div>
                                <n-select v-model:value="dataSetValue" filterable placeholder="选择数据包"
                                    :options="dataSetOptions" style="margin:5px 10px; flex:3" />
                                <n-button type='primary' style='margin:5px 10px; flex:1' @click="sendMessage">确认
                                </n-button>
                            </div>
                            <div class="drone-header-data-sender-desc">
                                <div class="drone-header-data-sender-desc-label">当前加密方式：</div>
                                <div class="drone-header-data-sender-desc-content">AES64</div>
                            </div>
                        </n-scrollbar>
                        <template #footer>
                            <div class="fill div">
                            </div>
                        </template>
                    </NCard>
                </n-grid-item>
            </n-grid>
        </div>
        <div class="drone-record">
            <NCard title="通信记录" :segmented="{ content: true, footer: true }" size="small" :bordered="false"
                style="height:400px">
                <n-data-table :columns="columns" :data="droneRecord" :pagination="pagination" :bordered="false"
                    class="record-table" />
            </NCard>

        </div>
    </div>
</template>
<script lang="ts" setup>
import { NScrollbar, NIcon, useMessage, NDataTable, NButton } from 'naive-ui';
// import type { MenuOption } from 'naive-ui'
import { ref, onMounted, h, Component, MenuInst } from 'vue';
import { useDroneStore } from '@/store/modules/drone';
import { sendMessageServer } from '@/api/dashboard'
import { BanOutline } from '@vicons/ionicons5'
import { PlanePrivate } from '@vicons/carbon';

const message = useMessage()
const droneStore = useDroneStore()

const loading = ref(true)
const droneOptions = ref([])
const dataSetOptions = ref([])
const dataSetValue = ref(null)
const droneNowId = ref(null)
const droneInfo = ref([])
const menuInstRef = ref<MenuInst | null>(null)

const columns = [
    {
        title: 'No',
        key: 'no',
        align: 'center'
    },
    {
        title: 'From',
        key: 'from',
        align: 'center'
    },
    {
        title: 'To',
        key: 'to',
        align: 'center'
    },
    {
        title: 'Time',
        key: 'time',
        align: 'center'
    },
    {
        title: 'Dataset',
        key: 'dataset',
        align: 'center'
    },
    {
        title: 'Action',
        key: 'action',
        render(row) {
            return h(
                NButton,
                {
                    strong: true,
                    tertiary: true,
                    size: 'small',
                    type: 'primary',
                    onClick: () => {
                        message.info('todo list')
                    }
                },
                { default: () => 'Delete' }
            )
        },
        align: 'center'
    }
]
const droneRecord = ref([])
const pagination = {
    pageSize: 5
}

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


function renderIcon(icon: Component) {
    return () => h(NIcon, null, { default: () => h(icon) })
}

function sendMessage() {
    if (droneNowId.value == null)
        message.info("请选择发送对象")
    else if (dataSetValue.value == null)
        message.error("请选择数据");
    else {
        const data = {
            from: 'Server',
            to: droneNowId.value,
            time: getTime(),
            dataset: dataSetValue.value
        }
        const response = sendMessageServer(data)
        response.then((res) => {
            message.success("发送成功")
        }).catch((error) => {
            console.log(error)
        })
    }

}

function handleUpdateValue(key: string) {
    droneNowId.value = key;
    // console.log(droneInfo.value[key])
    let newRecord = droneInfo.value[key].record
    let recordOption = []
    newRecord.forEach((item, index) => {
        recordOption.push({
            no: index,
            from: item.from,
            to: item.to,
            time: item.time,
            dataset: item.dataset
        })
    })
    droneRecord.value = recordOption
}

async function infoUpdate() {
    loading.value = true
    const data = await droneStore.getDroneInfo();
    droneInfo.value = data;
    let newOptions = [];
    if (data.length == 0) {
        newOptions.push({
            label: '无数据',
            key: -1,
            icon: renderIcon(BanOutline),
            disabled: true
        })
    }
    else {
        data.forEach((item) => {
            newOptions.push({
                label: '无人机 ' + item.id + ' 号',
                key: item.id,
                icon: renderIcon(PlanePrivate)
            })
        })
    }
    droneOptions.value = newOptions

    newOptions = []
    for (let i = 1; i <= 25; ++i) {
        newOptions.push({
            label: 'markSet' + String(i),
            value: i
        })
    }
    dataSetOptions.value = newOptions
    if (droneNowId.value != null) {
        menuInstRef.value?.showOption(droneNowId.value)
        handleUpdateValue(droneNowId.value)
    }
    loading.value = false
}

onMounted(async () => {
    const res = await infoUpdate()
    loading.value = false;
});
</script>

<style lang="less" scoped>
.drone-header {
    margin: 0;

    &-data-sender-container {
        display: flex;

        &-label {
            margin: auto;
            flex: 1;
            text-align: center;
        }
    }

    &-data-sender-desc {
        display: flex;
        margin-top: 10px;

        &-label {
            margin: auto;
            flex: 1;
            text-align: center;
        }

        &-content {
            margin: 5px 10px;
            flex: 4;
        }
    }
}

.drone-record {
    margin: 20px 0;
}

.record-table {
    min-height: 300px;
    max-height: 300px;
}
</style>
