import { Protected } from "@/components/auth/protected"; import { AccountView } from "@/features/account/account-view"; export default function Account(){return <Protected><AccountView/></Protected>}
