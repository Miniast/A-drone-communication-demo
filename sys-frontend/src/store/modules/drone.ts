import { defineStore } from 'pinia';
import { getDroneInfo } from '@/api/dashboard';

export interface IUserState {
    drones: any
}

export const useDroneStore = defineStore({
    id: 'app-drone',
    state: (): IUserState => ({
        drones: []
    }),
    getters: {
    },
    actions: {
        getDroneInfo() {
            let that = this;
            return new Promise((resolve, reject) => {
                getDroneInfo()
                    .then((res) => {
                        that.drones = res.data;
                        resolve(res);
                    })
                    .catch((error) => {
                        console.log(error)
                        reject(error);
                    });
            });
        }
    },
});

// // Need to be used outside the setup
// export function useUserStoreWidthOut() {
//     return useUserStore(store);
// }
