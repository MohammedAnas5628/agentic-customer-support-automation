"use client";
import { useEffect } from "react"; import { useRouter } from "next/navigation"; import { useAuth } from "@/lib/auth-provider";
export function Protected({children}:{children:React.ReactNode}){const{user,ready}=useAuth();const router=useRouter();useEffect(()=>{if(ready&&!user)router.replace("/login")},[ready,user,router]);if(!ready||!user)return <section className="shell grid min-h-[55vh] place-items-center"><div className="h-10 w-10 animate-spin rounded-full border-4 border-electric border-t-transparent" /></section>;return <>{children}</>}
