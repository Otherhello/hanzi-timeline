export default function Header() {
  return (
    <header className="header">
      <div className="header-text">
        <div className="kicker">字 形 演 变 · 证 据 链</div>
        <h1>汉字字形演变证据链时间轴</h1>
        <p className="subtitle">
          自甲骨文至楷书，逐期呈现字形，每一字必附实物出处与核对状态；
          无可靠实例者，明示「缺环」，不以后世字形倒填。
        </p>
      </div>
      <div className="seal" aria-hidden="true">证</div>
    </header>
  )
}
