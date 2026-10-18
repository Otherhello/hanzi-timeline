import type { VerificationStatus } from '../types'
import { VERIFICATION_LABEL } from '../data/eras'

export default function VerificationBadge({ status }: { status: VerificationStatus }) {
  return (
    <span className={`badge badge--${status}`}>
      <span className="badge-dot" />
      {VERIFICATION_LABEL[status]}
    </span>
  )
}
