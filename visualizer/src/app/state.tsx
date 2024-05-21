'use client'

import { Label, ShapeKey, View } from "@app/visual/type";
import { ViewStorage } from "@app/vql/storage";
import { goModelData } from "@app/visual/gotype";
import { Attrs, genGoModelData } from "@app/visual/model";
import { SplitDirection, WindowModel } from "@app/window/model";

import { createContext, useReducer } from "react";

export class GlobalState {
    // viewHistory: ViewStorage[]
    viewStorage: ViewStorage | undefined
    windowModel: WindowModel
    lastTime: number
    constructor(viewData?: View, viewStorage?: ViewStorage, windowModel?: WindowModel) {
        console.log('creat glob stat')
        // this.viewHistory = [];
        if (viewData === undefined) {
            this.viewStorage = viewStorage;
        } else {
            this.viewStorage = viewStorage || new ViewStorage(0, viewData);
        }
        this.windowModel = windowModel || new WindowModel();
        this.lastTime = 0;
    }
    getViewList(): string[] {
        if (this.viewStorage === undefined) {
            return [];
        }
        return Object.keys(this.viewStorage.data);
    }
    getGoModelData(viewDisplayed: string | undefined) {
        if (viewDisplayed === undefined || this.viewStorage === undefined) {
            return new goModelData();
        }
        return genGoModelData(this.viewStorage, viewDisplayed);
    }
    getGoModelDataFocused(viewDisplayed: string, objectKey: string) {
        if (this.viewStorage === undefined) {
            return new goModelData();
        }
        return genGoModelData(this.viewStorage, viewDisplayed, [objectKey]);
    }
    getAbstList(subviewName: string, objectKey: string) {
        if (this.viewStorage === undefined) {
            return [];
        }
        const subview = this.viewStorage.data[subviewName];
        const box = subview.pool.boxes[objectKey];
        if (!box) return [];
        return Object.keys(box.absts);
    }
    getAttrs(subviewName: string, objectKey: ShapeKey): Attrs {
        return this.viewStorage?.getAttrs(subviewName, objectKey) || {};
    }
    getMemberAttrs(subviewName: string, boxKey: ShapeKey, label: Label): Attrs {
        return this.viewStorage?.getMemberAttrs(subviewName, boxKey, label) || {};
    }
    getAttr(subviewName: string, objectKey: ShapeKey, attr: string): any {
        return this.getAttrs(subviewName, objectKey)[attr];
    }
    setAttr(subviewName: string, objectKey: ShapeKey, attr: string, value: any) {
        this.getAttrs(subviewName, objectKey)[attr] = value;
    }
    getAbst(subviewName: string, objectKey: ShapeKey): string {
        return this.getAttr(subviewName, objectKey, 'abst');
    }
    setAbst(subviewName: string, objectKey: ShapeKey, abstName: string) {
        this.setAttr(subviewName, objectKey, 'abst', abstName);
    }
    applyVql(subviewName: string, vqlCode: string) {
        this.viewStorage?.applyVql(subviewName, vqlCode);
    }
    clone() {
        let state = new GlobalState(undefined, this.viewStorage, this.windowModel);
        state.lastTime = this.lastTime;
        return state;
    }
    resetViewData(data: View) {
        let state = new GlobalState(data, undefined, this.windowModel);
        state.lastTime = this.lastTime;
        return state;
    }
}

const initialState = new GlobalState();

export type WindowModelAction =
    { type: 'SPLIT',   wKey: number, direction: SplitDirection }
  | { type: 'PICK',    viewDisplayed: string, objectKey: string }
  | { type: 'REMOVE',  wKey: number }
  | { type: 'ERASE',   wKey: number } // remove secondary
  | { type: 'REFRESH' }
  | { type: 'SETABST', viewName: string, objectKey: string, abstName: string }
  | { type: 'UPDATE',  wKey: number, viewName: string, vqlCode: string }

  export type WindowUIAction =
    { type: 'SWITCH',  wKey: number, viewName: string }
  | { type: 'FOCUS',   objectKey: string }

  export type GlobalStateAction = WindowModelAction | WindowUIAction
  | { type: 'INIT',    data: View }
 
// export const GlobalStatusContext = createContext(new GlobalStatus());
export const GlobalStateContext = createContext<{
    state: GlobalState;
    stateDispatch: React.Dispatch<GlobalStateAction>;
}>({
    state: initialState,
    stateDispatch: () => null
});

export function GlobalStateProvider({ dumpData, children }: { dumpData: View, children: React.ReactNode }) {
    const [state, stateDispatch] = useReducer(
        globalStateReducer,
        initialState
    );
    if (state == initialState) {
        // stateDispatch(new GlobalStateInit(dumpData));
        stateDispatch({ type: 'INIT', data: dumpData });
    }
    return (
        <GlobalStateContext.Provider value={{state, stateDispatch}}>
            {children}
        </GlobalStateContext.Provider>
    );
}

function globalStateReducer(state: GlobalState, action: GlobalStateAction) {
    switch (action.type) {
        case 'INIT':
            let orderedData = Object.keys(action.data).sort().reduce((obj: any, key) => { 
                obj[key] = action.data[key]; 
                return obj;
            }, {});
            return state.resetViewData(orderedData);
        case 'SPLIT': case 'REMOVE': case 'PICK': case 'ERASE':
        case 'REFRESH':
            windowModelReducer(state.windowModel, action);
            return state.clone();
        case 'SWITCH':
            state.windowModel.setViewDisplayed(action.wKey, action.viewName);
            return state.clone();
        case 'FOCUS':
            state.windowModel.focus(action.objectKey);
            return state;
        case 'SETABST':
            state.setAbst(action.viewName, action.objectKey, action.abstName);
            return state.clone();
        case 'UPDATE':
            console.log('UPDATE', action.viewName, action.vqlCode);
            try {
                state.applyVql(action.viewName, action.vqlCode);
            } catch (e: any) {
                console.log('vql error', e);
                state.windowModel.setConsoleText(action.wKey, e.message);
            }
            return state.clone();
        default:
            console.log('warning: unknown window model action', action);
            return state;
    }
}

function windowModelReducer(model: WindowModel, action: WindowModelAction): void {
    console.log('windowModelReducer', action);
    switch (action.type) {
        case 'SPLIT':   return model.split(action.wKey, action.direction);
        case 'REMOVE':  return model.remove(action.wKey);
        case 'PICK':    return model.pick(action.viewDisplayed, action.objectKey);
        case 'ERASE':   return model.erase(action.wKey);
        case 'REFRESH': return;
        default:
            console.log('warning: unknown window model action', action);
            return;
    }
}
