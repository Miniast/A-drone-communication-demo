<template>
    <div class="view-account">
        <div class="view-account-header"></div>
        <div class="view-account-container">
            <div class="view-account-top">
                <div class="view-account-top-logo">
                    <img src="~@/assets/images/logo.png" alt="" />
                    <p class="view-account-top-logo-desc">无人机控制系统</p>
                </div>
                <div class="view-account-top-desc">基于 Naive Ui Admin</div>
            </div>
            <div class="view-account-form">
                <n-form ref="formRef" label-placement="left" size="large" :model="formInline" :rules="rules">
                    <n-form-item path="username">
                        <n-input v-model:value="formInline.username" placeholder="请输入用户名">
                            <template #prefix>
                                <n-icon size="18" color="#808695">
                                    <PersonOutline />
                                </n-icon>
                            </template>
                        </n-input>
                    </n-form-item>
                    <n-form-item path="password">
                        <n-input v-model:value="formInline.password" type="password" showPasswordOn="click"
                            placeholder="请输入密码">
                            <template #prefix>
                                <n-icon size="18" color="#808695">
                                    <LockClosedOutline />
                                </n-icon>
                            </template>
                        </n-input>
                    </n-form-item>
                    <n-form-item>
                        <n-button type="primary" @click="handleSubmit" size="large" :loading="loading" block>
                            登录
                        </n-button>
                    </n-form-item>
                </n-form>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/store/modules/user';
import { useMessage } from 'naive-ui';
import { ResultEnum } from '@/enums/httpEnum';
import { PersonOutline, LockClosedOutline} from '@vicons/ionicons5';
import { PageEnum } from '@/enums/pageEnum';

interface FormState {
    username: string;
    password: string;
}

const formRef = ref();
const message = useMessage();
const loading = ref(false);
const LOGIN_NAME = PageEnum.BASE_LOGIN_NAME;

const formInline = reactive({
    username: 'admin',
    password: '123456',
    isCaptcha: true,
});

const rules = {
    username: { required: true, message: '请输入用户名', trigger: 'blur' },
    password: { required: true, message: '请输入密码', trigger: 'blur' },
};

const userStore = useUserStore();

const router = useRouter();
const route = useRoute();

const handleSubmit = (e) => {
    e.preventDefault();
    formRef.value.validate(async (errors) => {
        if (!errors) {
            const { username, password } = formInline;
            message.loading('登录中...');
            loading.value = true;

            const params: FormState = {
                username,
                password,
            };

            try {
                const { code, message: msg } = await userStore.login(params);
                console.log(code,msg);
                message.destroyAll();
                if (code == ResultEnum.SUCCESS) {
                    const toPath = decodeURIComponent((route.query?.redirect || '/') as string);
                    message.success('登录成功，即将进入系统');
                    if (route.name === LOGIN_NAME) {
                        router.replace('/');
                    } else router.replace(toPath);
                } else {
                    message.info(msg || '登录失败');
                }
            } finally {
                loading.value = false;
            }
        } else {
            message.error('请填写完整信息，并且进行验证码校验');
        }
    });
};
</script>

<style lang="less" scoped>
.view-account {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: auto;

    &-container {
        flex: 1;
        margin: 100px auto 200px;
        padding: 20px 40px;
        width: 500px;
        border-radius: 10px;
        background-color: rgba(250, 250, 250, 0.8);
    }

    &-top {
        padding: 20px 0;
        text-align: center;

        &-logo {
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow:hidden;
            white-space: nowrap;

            img {
                margin: 0 10px;
                width: 60px;
            }

            &-desc {
                margin: 0 10px;
                font-size:24px;
                font-weight:bold;
            }
        }

        &-desc {
            font-size: 14px;
            color: #000000;
        }
    }

    &-other {
        width: 100%;
    }

    .default-color {
        color: #515a6e;

        .ant-checkbox-wrapper {
            color: #515a6e;
        }
    }
}

@media (min-width: 768px) {
    .view-account {
        background-image: url('../../assets/images/login.jpg');
        background-repeat: no-repeat;
        background-position: 100%;
        background-size: 100%;
    }

    .page-account-container {
        padding: 32px 0 24px 0;
    }
}
</style>
