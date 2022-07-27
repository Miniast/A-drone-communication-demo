<template>
    <div>
        <div class="n-layout-page-header">
            <n-card :bordered="false" title="服务器面板">
                <n-grid cols="2 s:1 m:1 l:2 xl:2 2xl:2" responsive="screen">
                    <n-gi>
                        <div class="flex items-center">
                            <div>
                                <n-avatar circle :size="64" :src="avatar" />
                            </div>
                            <div>
                                <p class="px-4 text-xl">早安，MiniAst！</p>
                                <!-- <p class="px-4 text-gray-400">今日阴转大雨，15℃ - 25℃，出门记得带伞哦。</p> -->
                            </div>
                        </div>
                    </n-gi>
                    <n-gi>
                        <div class="flex justify-end w-full">
                            <div class="flex flex-1 flex-col justify-center text-right">
                                <span class="text-secondary">服务器状态</span>
                                <span class="text-2xl">{{ setupUpdated ? '已连接' : '获取中' }}</span>
                            </div>
                            <div class="flex flex-1 flex-col justify-center text-right">
                                <span class="text-secondary">最大连接数</span>
                                <span class="text-2xl">10</span>
                            </div>
                            <div class="flex flex-1 flex-col justify-center text-right">
                                <span class="text-secondary">当前连接数</span>
                                <span class="text-2xl">{{ setupUpdated ? droneNum + '/10' : '获取中' }}</span>
                            </div>
                        </div>
                    </n-gi>
                </n-grid>
            </n-card>
        </div>
    </div>
</template>

<script lang="ts" setup>
// import schoolboy from '@/assets/images/schoolboy.png';
import avatar from '@/assets/images/avatar.jpg';
import { useDroneStore } from '@/store/modules/drone';
import { ref, onMounted, onBeforeUnmount } from 'vue'

const droneStore = useDroneStore();

const setupUpdated = ref(false);
const droneNum = ref(null)
let droneUpdateTimer: any;


onMounted(() => {
    let droneUpdate = function () {
        const getInfo = droneStore.getDroneInfo();
        getInfo.then((res) => {
            droneNum.value = res.length
            setupUpdated.value = true;
        }).catch((error) => {
            console.log(error)
        })
        droneUpdateTimer = setTimeout(droneUpdate, 10000)
    }
    droneUpdate()
})
onBeforeUnmount(() => {
    clearTimeout(droneUpdateTimer)
})

</script>

<style lang="less" scoped>
.text-2xl {
    font-size: 20px;
}

.project-card {
    margin-right: -6px;

    &-item {
        margin: -1px;
        width: 33.333333%;
    }
}
</style>
